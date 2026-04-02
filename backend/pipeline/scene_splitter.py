import re
from ..config import settings
import logging

logger = logging.getLogger(__name__)

async def split_into_scenes(script: str, duration: int) -> list:
    """
    Split the script into 4-10 scenes based on duration.
    """
    # Simple split by sentences or paragraphs
    sentences = re.split(r'[.!?]\s+', script)
    num_scenes = min(max(len(sentences) // 2, settings.min_scenes), settings.max_scenes)
    
    scenes = []
    scene_length = len(sentences) // num_scenes
    for i in range(num_scenes):
        start = i * scene_length
        end = (i + 1) * scene_length if i < num_scenes - 1 else len(sentences)
        scene_text = ' '.join(sentences[start:end])
        scenes.append({
            "id": i + 1,
            "text": scene_text,
            "duration": duration // num_scenes
        })
    
    logger.info("Split script into %d scenes", len(scenes))
    return scenes