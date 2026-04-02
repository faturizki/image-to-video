from ..config import settings
import logging

logger = logging.getLogger(__name__)

async def generate_prompts(scenes: list, mode: str, reference_image: str = None) -> list:
    """
    Generate visual prompts for each scene with consistency.
    """
    prompts = []
    for scene in scenes:
        base_prompt = f"{scene['text']}, {mode} style"
        if reference_image:
            base_prompt += f", featuring the same character from reference image"
        consistency = "same character, consistent identity, cinematic lighting, high detail"
        full_prompt = f"{base_prompt}, {consistency}"
        prompts.append(full_prompt)
    
    logger.info("Generated prompts for %d scenes", len(prompts))
    return prompts