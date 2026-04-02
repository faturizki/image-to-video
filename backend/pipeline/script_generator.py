import openai
from ..config import settings
import logging

logger = logging.getLogger(__name__)

async def generate_script(prompt: str, mode: str) -> str:
    """
    Generate a narrative script from the prompt.
    """
    if settings.openai_api_key:
        try:
            client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a script writer for {mode} videos. Create a detailed narrative script."},
                    {"role": "user", "content": f"Write a script based on this prompt: {prompt}"}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error("OpenAI error: %s", e)
            return mock_script(prompt, mode)
    else:
        return mock_script(prompt, mode)

def mock_script(prompt: str, mode: str) -> str:
    """
    Mock script generation.
    """
    if mode == "ads":
        return f"Scene 1: Introduction to {prompt}. Scene 2: Benefits explained. Scene 3: Call to action."
    else:
        return f"Cinematic opening: {prompt}. Dramatic scenes unfold. Emotional climax. Resolution."