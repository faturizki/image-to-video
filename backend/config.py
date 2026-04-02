import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

# Constants
DEFAULT_DURATION = 180  # seconds
MAX_SCENES = 10
MIN_SCENES = 4
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

class Settings(BaseSettings):
    # API Keys - Let BaseSettings handle environment loading
    huggingface_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

    # Paths - Relative paths from backend directory
    assets_dir: str = "../assets"
    outputs_dir: str = "../outputs"

    # FFmpeg path
    ffmpeg_path: str = "ffmpeg"

    # Default settings
    default_duration: int = DEFAULT_DURATION
    max_scenes: int = MAX_SCENES
    min_scenes: int = MIN_SCENES

    class Config:
        env_file = ".env"  # Load from .env file if exists
        env_file_encoding = "utf-8"

    def __init__(self, **data):
        super().__init__(**data)
        # Directory creation moved to runtime to avoid permission issues
        # Validate API keys
        if self.huggingface_api_key:
            print("Hugging Face API key loaded successfully")
        else:
            print("WARNING: HUGGINGFACE_API_KEY not found - using mock mode")

        if self.openai_api_key:
            print("OpenAI API key loaded successfully")
        else:
            print("WARNING: OPENAI_API_KEY not found - using mock mode")

        if self.gemini_api_key:
            print("Gemini API key loaded successfully")
        else:
            print("WARNING: GEMINI_API_KEY not found - using mock mode")

        # Production validation
        if os.getenv("ENV") == "production" and not self.huggingface_api_key:
            raise ValueError("HUGGINGFACE_API_KEY is required in production environment")

settings = Settings()