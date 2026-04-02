import asyncio
import os
from .script_generator import generate_script
from .scene_splitter import split_into_scenes
from .prompt_engine import generate_prompts
from .image_generator import generate_images
from .video_generator import generate_videos
from .merger import merge_videos
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_pipeline(prompt: str, mode: str, duration: int, reference_image: str = None):
    """
    Main pipeline to generate video from prompt.
    """
    logger.info("Starting pipeline for prompt: %s", prompt)

    # Step 1: Generate script
    script = await generate_script(prompt, mode)
    logger.info("Script generated: %s", script[:100] + "...")

    # Step 2: Split into scenes
    scenes = await split_into_scenes(script, duration)
    logger.info("Split into %d scenes", len(scenes))

    # Step 3: Generate prompts for each scene
    prompts = await generate_prompts(scenes, mode, reference_image)
    logger.info("Prompts generated for scenes")

    # Step 4: Generate images
    image_files = await generate_images(prompts)
    logger.info("Images generated: %d files", len(image_files))

    # Step 4b: Generate videos from images
    video_files = await generate_videos(image_files)
    logger.info("Videos generated: %d files", len(video_files))

    # Step 5: Generate voice (optional, placeholder)
    voice_files = []  # Placeholder

    # Step 6: Merge videos
    video_path = await merge_videos(video_files, voice_files, duration)
    logger.info("Video merged: %s", video_path)

    return {
        "video_url": f"/outputs/{os.path.basename(video_path)}",
        "scenes": scenes
    }