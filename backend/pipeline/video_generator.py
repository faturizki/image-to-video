import ffmpeg
import os
import asyncio
from typing import List
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
import logging
import subprocess

logger = logging.getLogger(__name__)

async def generate_videos(media_files: List[str]) -> List[str]:
    """
    Generate videos from images (simple slideshow).
    """
    if not media_files:
        raise ValueError("Media files list cannot be empty")

    video_files = []

    # Check if FFmpeg is available
    ffmpeg_available = await _check_ffmpeg()
    if not ffmpeg_available:
        logger.warning("[VIDEO] FFmpeg not available, returning image files as videos")
        return media_files

    for i, img_path in enumerate(media_files):
        if not os.path.exists(img_path):
            logger.error(f"[VIDEO] Image file not found: {img_path}")
            continue

        video_path = img_path.replace('.png', '.mp4')
        try:
            await _create_video_from_image(img_path, video_path)
            if os.path.exists(video_path):
                video_files.append(video_path)
                logger.info(f"[VIDEO] Created video: {video_path}")
            else:
                logger.error(f"[VIDEO] Video creation failed: {video_path}")
        except Exception as e:
            logger.error(f"[VIDEO] Failed to create video for {img_path}: {e}")

    if len(video_files) != len(media_files):
        logger.warning(f"[VIDEO] Generated {len(video_files)} videos, expected {len(media_files)}")

    logger.info(f"[VIDEO] Generated {len(video_files)} videos")
    return video_files

async def _check_ffmpeg() -> bool:
    """
    Check if FFmpeg is available.
    """
    try:
        result = await asyncio.create_subprocess_exec(
            'ffmpeg', '-version',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await result.wait()
        return result.returncode == 0
    except (OSError, FileNotFoundError):
        return False

async def _create_video_from_image(img_path: str, video_path: str):
    """
    Create a video from a single image using FFmpeg.
    """
    # Use asyncio to run FFmpeg asynchronously
    process = await asyncio.create_subprocess_exec(
        'ffmpeg', '-y', '-loop', '1', '-i', img_path, '-t', '5',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await process.wait()
    if process.returncode != 0:
        stdout, stderr = await process.communicate()
        raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")