from typing import List, Dict, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
import logging

logger = logging.getLogger(__name__)

# Consistent prompt template
PROMPT_TEMPLATE = "same character, consistent identity, same face, cinematic lighting, high detail, 4k"

async def generate_prompts(scenes: List[Dict[str, Any]], mode: str, reference_image: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Generate visual prompts for each scene with consistency.
    Modifies scenes in-place to add 'prompt' key.
    """
    if not scenes:
        raise ValueError("Scenes list cannot be empty")
    if mode not in ["ads", "cinematic"]:
        raise ValueError("Mode must be 'ads' or 'cinematic'")

    for scene in scenes:
        if 'text' not in scene or not scene['text'].strip():
            raise ValueError(f"Scene {scene.get('scene', 'unknown')} has no text")

        base_prompt = f"{scene['text']}, {mode} style"
        if reference_image:
            base_prompt += ", featuring the same character from reference image"

        full_prompt = f"{base_prompt}, {PROMPT_TEMPLATE}"
        scene['prompt'] = full_prompt

    logger.info(f"[PROMPT] Generated prompts for {len(scenes)} scenes")
    return scenes