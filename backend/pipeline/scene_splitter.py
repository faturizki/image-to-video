import re
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
import logging

logger = logging.getLogger(__name__)

async def split_into_scenes(script: str, duration: int) -> List[Dict[str, Any]]:
    """
    Split the script into 4-10 scenes based on duration.
    Returns list of dicts with scene, text, duration.
    """
    if not script or not script.strip():
        raise ValueError("Script cannot be empty")
    if duration <= 0:
        raise ValueError("Duration must be positive")

    # Simple split by sentences or paragraphs
    sentences = re.split(r'[.!?]\s+', script.strip())
    if not sentences:
        raise ValueError("No sentences found in script")

    # Calculate number of scenes
    num_scenes = min(max(len(sentences) // 2, settings.min_scenes), settings.max_scenes)
    scene_duration = duration // num_scenes

    scenes = []
    scene_length = len(sentences) // num_scenes
    for i in range(num_scenes):
        start = i * scene_length
        end = (i + 1) * scene_length if i < num_scenes - 1 else len(sentences)
        scene_text = ' '.join(sentences[start:end]).strip()
        if not scene_text:
            scene_text = f"Scene {i+1} content"  # Fallback

        scenes.append({
            "scene": i + 1,
            "text": scene_text,
            "duration": scene_duration
        })

    logger.info(f"[SCENE] Split script into {len(scenes)} scenes")
    return scenes