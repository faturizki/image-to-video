import ffmpeg
import os
from ..config import settings
import logging
import subprocess

logger = logging.getLogger(__name__)

async def generate_videos(media_files: list) -> list:
    """
    Generate videos from images (simple slideshow).
    """
    video_files = []
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("FFmpeg not available, mocking videos")
        # Mock: just return the image files as "videos"
        return media_files

    for i, img_path in enumerate(media_files):
        video_path = img_path.replace('.png', '.mp4')
        # Create a 5-second video from image
        ffmpeg.input(img_path, loop=1, t=5).output(video_path, vcodec='libx264', pix_fmt='yuv420p').run()
        video_files.append(video_path)
    
    logger.info("Generated %d videos", len(video_files))
    return video_files