import requests
from PIL import Image, ImageDraw
import os
from ..config import settings
import logging

logger = logging.getLogger(__name__)

async def generate_images(prompts: list) -> list:
    """
    Generate images for each prompt using Hugging Face or mock.
    """
    media_files = []
    for i, prompt in enumerate(prompts):
        if settings.huggingface_api_key:
            # Placeholder for Hugging Face API call
            # Assume using Stable Diffusion or similar
            # For now, mock
            pass
        # Mock: create a placeholder image
        img = Image.new('RGB', (512, 512), color='gray')
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), f"Scene {i+1}: {prompt[:50]}...", fill='white')
        
        filename = f"scene_{i+1}.png"
        filepath = os.path.join(settings.outputs_dir, filename)
        img.save(filepath)
        media_files.append(filepath)
    
    logger.info("Generated %d images", len(media_files))
    return media_files