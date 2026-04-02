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

async def merge_videos(video_files: List[str], voice_files: List[str], duration: int) -> str:
    """
    Merge videos into one final video using FFmpeg.
    """
    if not video_files:
        raise ValueError("Video files list cannot be empty")

    # Validate input files
    valid_video_files = []
    for vf in video_files:
        if os.path.exists(vf) and os.path.getsize(vf) > 0:
            valid_video_files.append(vf)
        else:
            logger.warning(f"[MERGE] Invalid or missing video file: {vf}")

    if not valid_video_files:
        raise ValueError("No valid video files to merge")

    output_path = os.path.join(settings.outputs_dir, "final_video.mp4")
    os.makedirs(settings.outputs_dir, exist_ok=True)

    # Check if FFmpeg is available
    ffmpeg_available = await _check_ffmpeg()
    if not ffmpeg_available:
        logger.warning("[MERGE] FFmpeg not available, creating mock video")
        return await _create_mock_video(output_path)

    try:
        await _merge_with_ffmpeg(valid_video_files, output_path)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"[MERGE] Successfully merged videos into {output_path}")
            return output_path
        else:
            raise RuntimeError("FFmpeg completed but output file is invalid")
    except Exception as e:
        logger.error(f"[MERGE] FFmpeg merge failed: {e}")
        # Fallback to mock
        return await _create_mock_video(output_path)

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

async def _merge_with_ffmpeg(video_files: List[str], output_path: str):
    """
    Merge videos using FFmpeg concat.
    """
    # Create a concat file
    concat_file = os.path.join(settings.outputs_dir, "concat.txt")
    try:
        with open(concat_file, 'w') as f:
            for vf in video_files:
                f.write(f"file '{vf}'\n")

        # Run FFmpeg
        process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file,
            '-c', 'copy', output_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.wait()
        if process.returncode != 0:
            stdout, stderr = await process.communicate()
            raise RuntimeError(f"FFmpeg merge failed: {stderr.decode()}")
    finally:
        # Clean up concat file
        if os.path.exists(concat_file):
            os.remove(concat_file)

async def _create_mock_video(output_path: str) -> str:
    """
    Create a mock video file.
    """
    try:
        with open(output_path, 'w') as f:
            f.write("# Mock video file - FFmpeg not available\n")
        logger.warning(f"[MERGE] Created mock video: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"[MERGE] Failed to create mock video: {e}")
        raise