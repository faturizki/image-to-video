import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Paths
    assets_dir: str = "/workspaces/image-to-video/assets"
    outputs_dir: str = "/workspaces/image-to-video/outputs"

    # FFmpeg path
    ffmpeg_path: str = "ffmpeg"

    # Default settings
    default_duration: int = 180  # seconds
    max_scenes: int = 10
    min_scenes: int = 4

    class Config:
        env_file = ".env"

settings = Settings()