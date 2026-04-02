import google.generativeai as genai
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
import logging

logger = logging.getLogger(__name__)

async def generate_script(prompt: str, mode: str) -> str:
    """
    Generate a narrative script from the prompt.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    if mode not in ["ads", "cinematic"]:
        raise ValueError("Mode must be 'ads' or 'cinematic'")

    if settings.gemini_api_key:
        try:
            logger.info("[SCRIPT] Using Gemini API for script generation")
            genai.configure(api_key=settings.gemini_api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")  # Note: Using 1.5-flash as 2.5-flash might not be available yet
            response = model.generate_content(
                f"You are a script writer for {mode} videos. Create a detailed narrative script based on this prompt: {prompt}"
            )
            script = response.text.strip()
            if not script:
                raise ValueError("Gemini returned empty script")
            logger.info("[SCRIPT] Script generated via Gemini")
            return script
        except Exception as e:
            logger.warning(f"[SCRIPT] Gemini failed: {e}, falling back to mock")
            return mock_script(prompt, mode)
    else:
        logger.info("[SCRIPT] Using mock script generation")
        return mock_script(prompt, mode)

def mock_script(prompt: str, mode: str) -> str:
    """
    Mock script generation.
    """
    if mode == "ads":
        return f"Scene 1: Introduction to {prompt}. Scene 2: Benefits explained. Scene 3: Call to action."
    else:
        return f"Cinematic opening: {prompt}. Dramatic scenes unfold. Emotional climax. Resolution."