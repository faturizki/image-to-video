import ffmpeg
import os
from ..config import settings
import logging
import subprocess

logger = logging.getLogger(__name__)

async def merge_videos(video_files: list, voice_files: list, duration: int) -> str:
    """
    Merge videos into one final video using FFmpeg.
    """
    # Check if FFmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("FFmpeg not available, creating mock video")
        # Mock: create a dummy video file
        output_path = os.path.join(settings.outputs_dir, "final_video.mp4")
        with open(output_path, 'w') as f:
            f.write("Mock video file")
        return output_path

    # Create a concat file
    concat_file = os.path.join(settings.outputs_dir, "concat.txt")
    with open(concat_file, 'w') as f:
        for vf in video_files:
            f.write(f"file '{vf}'\n")
    
    output_path = os.path.join(settings.outputs_dir, "final_video.mp4")
    ffmpeg.input(concat_file, format='concat', safe=0).output(output_path, c='copy').run()
    
    # Clean up
    os.remove(concat_file)
    
    logger.info("Merged videos into %s", output_path)
    return output_path