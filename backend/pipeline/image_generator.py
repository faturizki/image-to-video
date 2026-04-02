import requests
from PIL import Image, ImageDraw
import os
from typing import List
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

async def generate_images(prompts: List[str]) -> List[str]:
    """
    Generate images for each prompt using Hugging Face or mock.
    """
    if not prompts:
        raise ValueError("Prompts list cannot be empty")

    media_files = []
    for i, prompt in enumerate(prompts):
        filepath = await _generate_single_image(prompt, i + 1)
        if filepath and os.path.exists(filepath):
            media_files.append(filepath)
        else:
            logger.error(f"[IMAGE] Failed to generate image for scene {i+1}")
            # Create fallback image
            fallback_path = await _create_fallback_image(prompt, i + 1)
            media_files.append(fallback_path)

    if len(media_files) != len(prompts):
        logger.warning(f"[IMAGE] Generated {len(media_files)} images, expected {len(prompts)}")

    logger.info(f"[IMAGE] Generated {len(media_files)} images")
    return media_files

async def _generate_single_image(prompt: str, scene_num: int) -> str:
    """
    Generate a single image with retry logic.
    """
    filename = f"scene_{scene_num}.png"
    filepath = os.path.join(settings.outputs_dir, filename)

    # Try Hugging Face API first
    if settings.huggingface_api_key:
        logger.info(f"[IMAGE] Attempting Hugging Face generation for scene {scene_num} (API key available)")
        for attempt in range(3):  # Retry up to 3 times
            try:
                logger.info(f"[IMAGE] Attempting Hugging Face generation for scene {scene_num} (attempt {attempt+1})")
                # Placeholder for actual Hugging Face API call
                # For now, fall through to mock
                break
            except Exception as e:
                logger.warning(f"[IMAGE] Hugging Face attempt {attempt+1} failed: {e}")
                if attempt == 2:
                    logger.error(f"[IMAGE] Hugging Face failed after 3 attempts for scene {scene_num}")
    else:
        logger.info(f"[IMAGE] Hugging Face API key not available, using mock for scene {scene_num}")

    # Fallback to mock generation
    return await _create_mock_image(prompt, scene_num)

async def _create_mock_image(prompt: str, scene_num: int) -> str:
    """
    Create a mock placeholder image.
    """
    try:
        img = Image.new('RGB', (512, 512), color='gray')
        draw = ImageDraw.Draw(img)
        # Wrap text
        words = prompt.split()
        lines = []
        current_line = ""
        for word in words[:10]:  # Limit words
            if len(current_line + word) < 40:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())

        y = 10
        for line in lines:
            draw.text((10, y), line, fill='white')
            y += 20

        filename = f"scene_{scene_num}.png"
        filepath = os.path.join(settings.outputs_dir, filename)
        os.makedirs(settings.outputs_dir, exist_ok=True)
        img.save(filepath)
        logger.info(f"[IMAGE] Created mock image: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"[IMAGE] Failed to create mock image: {e}")
        raise

async def _create_fallback_image(prompt: str, scene_num: int) -> str:
    """
    Create a simple fallback image.
    """
    try:
        img = Image.new('RGB', (512, 512), color='red')
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), f"Fallback Scene {scene_num}", fill='white')

        filename = f"scene_{scene_num}_fallback.png"
        filepath = os.path.join(settings.outputs_dir, filename)
        os.makedirs(settings.outputs_dir, exist_ok=True)
        img.save(filepath)
        logger.warning(f"[IMAGE] Created fallback image: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"[IMAGE] Failed to create fallback image: {e}")
        raise