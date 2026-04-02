from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from .config import settings
from .pipeline import run_pipeline

app = FastAPI(title="AI Video Generator", version="1.0.0")

class GenerateRequest(BaseModel):
    prompt: str
    mode: str  # "ads" or "cinematic"
    duration: int = 180  # seconds
    reference_image: str = None  # optional URL or path

class GenerateResponse(BaseModel):
    status: str
    video_url: str
    scenes: list

@app.post("/generate", response_model=GenerateResponse)
async def generate_video(request: GenerateRequest, reference_image: UploadFile = File(None)):
    try:
        # Save reference image if provided
        ref_image_path = None
        if reference_image:
            ref_image_path = os.path.join(settings.assets_dir, reference_image.filename)
            with open(ref_image_path, "wb") as f:
                f.write(await reference_image.read())

        # Run the pipeline
        result = await run_pipeline(
            prompt=request.prompt,
            mode=request.mode,
            duration=request.duration,
            reference_image=ref_image_path
        )

        return GenerateResponse(
            status="success",
            video_url=result["video_url"],
            scenes=result["scenes"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/outputs/{filename}")
async def get_output(filename: str):
    file_path = os.path.join(settings.outputs_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='video/mp4')
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)