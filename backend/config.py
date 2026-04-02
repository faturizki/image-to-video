import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Constants
DEFAULT_DURATION = 180  # seconds
MAX_SCENES = 10
MIN_SCENES = 4
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

class Settings(BaseSettings):
    # API Keys
    huggingface_api_key: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Paths
    assets_dir: str = "/workspaces/image-to-video/assets"
    outputs_dir: str = "/workspaces/image-to-video/outputs"

    # FFmpeg path
    ffmpeg_path: str = "ffmpeg"

    # Default settings
    default_duration: int = DEFAULT_DURATION
    max_scenes: int = MAX_SCENES
    min_scenes: int = MIN_SCENES

    class Config:
        env_file = ".env"

    def __init__(self, **data):
        super().__init__(**data)
        # Validate and create directories
        Path(self.assets_dir).mkdir(parents=True, exist_ok=True)
        Path(self.outputs_dir).mkdir(parents=True, exist_ok=True)

        # Validate API keys (optional, can be None for mock mode)
        if self.huggingface_api_key:
            print("Hugging Face API key loaded successfully")
        else:
            print("Hugging Face API key not found - using mock mode")

        if self.openai_api_key:
            print("OpenAI API key loaded successfully")
        else:
            print("OpenAI API key not found - using mock mode")

        # For production deployment, require Hugging Face API key
        if os.getenv("ENV") == "production" and not self.huggingface_api_key:
            raise ValueError("HUGGINGFACE_API_KEY is required in production environment")

settings = Settings()