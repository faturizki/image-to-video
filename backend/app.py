from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import logging
from typing import Optional, List
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from pipeline.run_pipeline import run_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Video Generator", version="1.0.0")

class GenerateRequest(BaseModel):
    prompt: str
    mode: str  # "ads" or "cinematic"
    duration: int = 180  # seconds
    reference_image: Optional[str] = None  # optional URL or path

class SceneData(BaseModel):
    scene: int
    text: str
    duration: int
    prompt: str

class GenerateResponse(BaseModel):
    status: str
    video_url: str
    scenes: List[SceneData]

@app.post("/generate", response_model=GenerateResponse)
async def generate_video(request: GenerateRequest, reference_image: UploadFile = File(None)):
    logger.info(f"Received generate request: prompt='{request.prompt[:50]}...', mode={request.mode}, duration={request.duration}")
    
    try:
        # Validate input
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        if request.mode not in ["ads", "cinematic"]:
            raise HTTPException(status_code=400, detail="Mode must be 'ads' or 'cinematic'")
        if not (120 <= request.duration <= 300):
            raise HTTPException(status_code=400, detail="Duration must be between 120 and 300 seconds")

        # Save reference image if provided
        ref_image_path: Optional[str] = None
        if reference_image:
            if not reference_image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise HTTPException(status_code=400, detail="Reference image must be PNG or JPG")
            ref_image_path = os.path.join(settings.assets_dir, reference_image.filename)
            os.makedirs(settings.assets_dir, exist_ok=True)
            with open(ref_image_path, "wb") as f:
                content = await reference_image.read()
                if len(content) > 10 * 1024 * 1024:  # 10MB limit
                    raise HTTPException(status_code=400, detail="Reference image too large (max 10MB)")
                f.write(content)
            logger.info(f"Saved reference image: {ref_image_path}")

        # Run the pipeline
        result = await run_pipeline(
            prompt=request.prompt,
            mode=request.mode,
            duration=request.duration,
            reference_image=ref_image_path
        )

        logger.info(f"Pipeline completed successfully, video: {result['video_url']}")
        return GenerateResponse(
            status="success",
            video_url=result["video_url"],
            scenes=result["scenes"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/outputs/{filename}")
async def get_output(filename: str):
    if not filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_path = os.path.join(settings.outputs_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    logger.info(f"Serving file: {file_path}")
    return FileResponse(file_path, media_type='video/mp4')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)