import asyncio
import os
from typing import List, Dict, Any, Optional
from .script_generator import generate_script
from .scene_splitter import split_into_scenes
from .prompt_engine import generate_prompts
from .image_generator import generate_images
from .video_generator import generate_videos
from .merger import merge_videos
import logging

logger = logging.getLogger(__name__)

async def run_pipeline(prompt: str, mode: str, duration: int, reference_image: Optional[str] = None) -> Dict[str, Any]:
    """
    Main pipeline to generate video from prompt.
    """
    logger.info(f"[PIPELINE] Starting pipeline for prompt: '{prompt[:50]}...', mode: {mode}, duration: {duration}s")

    try:
        # Step 1: Generate script
        logger.info("[STEP] Generating script...")
        script = await generate_script(prompt, mode)
        if not script or not script.strip():
            raise ValueError("Script generation failed: empty script")
        logger.info(f"[STEP] Script generated: {len(script)} characters")

        # Step 2: Split into scenes
        logger.info("[STEP] Splitting into scenes...")
        scenes = await split_into_scenes(script, duration)
        if not scenes or len(scenes) == 0:
            raise ValueError("Scene splitting failed: no scenes generated")
        logger.info(f"[STEP] Split into {len(scenes)} scenes")

        # Step 3: Generate prompts for each scene
        logger.info("[STEP] Generating prompts...")
        scenes_with_prompts = await generate_prompts(scenes, mode, reference_image)
        if len(scenes_with_prompts) != len(scenes):
            raise ValueError("Prompt generation failed: mismatch in scene count")
        logger.info(f"[STEP] Prompts generated for {len(scenes_with_prompts)} scenes")

        # Extract prompts for generation
        prompts = [scene['prompt'] for scene in scenes_with_prompts]

        # Step 4: Generate images
        logger.info("[STEP] Generating images...")
        image_files = await generate_images(prompts)
        if len(image_files) != len(prompts):
            raise ValueError("Image generation failed: mismatch in file count")
        logger.info(f"[STEP] Generated {len(image_files)} images")

        # Step 5: Generate videos from images
        logger.info("[STEP] Generating videos...")
        video_files = await generate_videos(image_files)
        if len(video_files) != len(image_files):
            raise ValueError("Video generation failed: mismatch in file count")
        logger.info(f"[STEP] Generated {len(video_files)} videos")

        # Step 6: Generate voice (optional, placeholder)
        voice_files: List[str] = []  # Placeholder for future voice generation

        # Step 7: Merge videos
        logger.info("[STEP] Merging videos...")
        video_path = await merge_videos(video_files, voice_files, duration)
        if not video_path or not os.path.exists(video_path):
            raise ValueError("Video merging failed: output file not created")
        logger.info(f"[STEP] Video merged successfully: {video_path}")

        result = {
            "video_url": f"/outputs/{os.path.basename(video_path)}",
            "scenes": scenes_with_prompts
        }
        logger.info("[PIPELINE] Pipeline completed successfully")
        return result

    except Exception as e:
        logger.error(f"[PIPELINE] Pipeline failed: {str(e)}", exc_info=True)
        # Return partial result if possible, or raise
        raise RuntimeError(f"Pipeline execution failed: {str(e)}") from e