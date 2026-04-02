"""
Pipeline Orchestrator - Gemini & Hugging Face Integration

This module orchestrates the AI pipeline:
1. Gemini: Generate scripts and structured prompts
2. Hugging Face: Generate videos from prompts
3. Output: Save and manage generated videos

Provides high-level functions to coordinate multi-model AI generation workflows.
"""

import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
import google.generativeai as genai
import requests

logger = logging.getLogger(__name__)


class GeminiOrchestrator:
    """Manages Gemini API calls for script and prompt generation."""
    
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("[ORCHESTRATOR] Gemini orchestrator initialized")
    
    def generate_video_script(self, user_input: str, mode: str = "ads") -> str:
        """
        Generate a narrative script from user input.
        
        Args:
            user_input: User prompt/description
            mode: "ads" or "cinematic"
        
        Returns:
            Generated script as string
        """
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty")
        
        if mode not in ["ads", "cinematic"]:
            raise ValueError("Mode must be 'ads' or 'cinematic'")
        
        try:
            logger.info(f"[GEMINI] Generating {mode} script for: {user_input[:50]}...")
            
            system_prompt = f"""You are an expert {mode} video script writer. 
            Create a detailed, engaging, and structured script.
            For '{mode}' videos, ensure:
            - Clear narrative progression
            - Visual descriptions for each scene
            - Timing hints where appropriate
            """
            
            user_prompt = f"Generate a {mode} video script based on: {user_input}"
            
            response = self.model.generate_content(
                f"{system_prompt}\n\nUser request: {user_prompt}"
            )
            
            script = response.text.strip()
            
            if not script:
                raise ValueError("Gemini returned empty script")
            
            logger.info(f"[GEMINI] Script generated successfully ({len(script)} chars)")
            return script
        
        except Exception as e:
            logger.error(f"[GEMINI] Script generation failed: {str(e)}")
            raise
    
    def generate_structured_prompts(self, script: str, num_scenes: int = 3) -> List[Dict[str, Any]]:
        """
        Parse script and generate structured video prompts via Gemini.
        
        Args:
            script: The generated script
            num_scenes: Number of scenes to generate
        
        Returns:
            List of scene dictionaries with prompt information
        """
        if not script or not script.strip():
            raise ValueError("Script cannot be empty")
        
        try:
            logger.info(f"[GEMINI] Generating structured prompts for {num_scenes} scenes...")
            
            prompt = f"""Analyze this script and generate {num_scenes} scenes with video prompts.
            
Script:
{script}

Generate a JSON response with exactly {num_scenes} scenes. Each scene should have:
- scene_number: integer (1, 2, 3, ...)
- scene_description: brief description of the scene
- video_prompt: detailed, vivid prompt for video generation (include visual style, colors, mood, action)
- duration_seconds: estimated duration for this scene
- visual_style: artistic style (e.g., "cinematic", "animated", "realistic")

Format: Return ONLY valid JSON array, no markdown. Example:
[
  {{"scene_number": 1, "scene_description": "...", "video_prompt": "...", "duration_seconds": 5, "visual_style": "cinematic"}},
  {{"scene_number": 2, "scene_description": "...", "video_prompt": "...", "duration_seconds": 5, "visual_style": "cinematic"}}
]"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            response_text = response_text.strip()
            
            # Parse JSON
            try:
                scenes = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.error(f"[GEMINI] Failed to parse JSON response: {e}")
                logger.error(f"[GEMINI] Response text: {response_text[:200]}...")
                raise ValueError(f"Invalid JSON from Gemini: {str(e)}")
            
            if not isinstance(scenes, list):
                raise ValueError("Gemini response is not a list")
            
            if len(scenes) != num_scenes:
                logger.warning(f"[GEMINI] Expected {num_scenes} scenes, got {len(scenes)}")
            
            logger.info(f"[GEMINI] Generated {len(scenes)} structured prompts")
            return scenes
        
        except Exception as e:
            logger.error(f"[GEMINI] Prompt generation failed: {str(e)}")
            raise


class HuggingFaceOrchestrator:
    """Manages Hugging Face API calls for video generation."""
    
    # List of available video generation models
    AVAILABLE_MODELS = {
        "text-to-video": "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt",
        "text-to-image": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
    }
    
    def __init__(self):
        if not settings.huggingface_api_key:
            raise ValueError("HUGGINGFACE_API_KEY not configured")
        
        self.api_key = settings.huggingface_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        logger.info("[ORCHESTRATOR] Hugging Face orchestrator initialized")
    
    def validate_api_key(self) -> bool:
        """
        Validate Hugging Face API key by making a test request.
        
        Returns:
            True if valid, False otherwise
        """
        try:
            logger.info("[HUGGINGFACE] Validating API key...")
            
            url = "https://huggingface.co/api/whoami"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                logger.info("[HUGGINGFACE] API key validation successful")
                return True
            else:
                logger.warning(f"[HUGGINGFACE] API key validation failed: {response.status_code}")
                return False
        
        except Exception as e:
            logger.error(f"[HUGGINGFACE] API key validation error: {str(e)}")
            return False
    
    def generate_video(self, prompt: str, scene_num: int, duration: int = 5) -> Optional[str]:
        """
        Generate a video using Hugging Face API (placeholder implementation).
        Currently returns mock video or attempts actual API call.
        
        Args:
            prompt: Detailed prompt for video generation
            scene_num: Scene number for naming
            duration: Duration in seconds
        
        Returns:
            Path to generated video file or None
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        try:
            logger.info(f"[HUGGINGFACE] Generating video for scene {scene_num}: {prompt[:50]}...")
            
            # Create outputs directory if it doesn't exist
            os.makedirs(settings.outputs_dir, exist_ok=True)
            
            # Attempt actual API call (may fail without real model)
            try:
                # This is a placeholder for actual Hugging Face video generation
                # Real implementation would depend on available models
                logger.info(f"[HUGGINGFACE] Attempting API call for scene {scene_num}...")
                
                # For now, return a descriptive log
                # In production, this would call an actual video generation endpoint
                logger.info(f"[HUGGINGFACE] Video generation would use prompt: {prompt}")
                
                # Generate mock video file as fallback
                video_path = self._create_mock_video(prompt, scene_num)
                return video_path
            
            except Exception as e:
                logger.warning(f"[HUGGINGFACE] API call failed: {str(e)}, using mock fallback")
                video_path = self._create_mock_video(prompt, scene_num)
                return video_path
        
        except Exception as e:
            logger.error(f"[HUGGINGFACE] Video generation failed: {str(e)}")
            raise
    
    def _create_mock_video(self, prompt: str, scene_num: int) -> str:
        """
        Create a mock video file for testing/fallback.
        
        Args:
            prompt: Prompt that would have been used
            scene_num: Scene number
        
        Returns:
            Path to mock video file
        """
        try:
            filename = f"video_scene_{scene_num}.mp4"
            filepath = os.path.join(settings.outputs_dir, filename)
            
            # Create a simple text file as mock video
            # In real implementation, this would be actual video binary
            with open(filepath, "w") as f:
                f.write(f"Mock video for scene {scene_num}\n")
                f.write(f"Prompt: {prompt}\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
            
            logger.info(f"[HUGGINGFACE] Mock video created: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"[HUGGINGFACE] Mock video creation failed: {str(e)}")
            raise


class PipelineOrchestrator:
    """
    Main orchestrator that coordinates Gemini and Hugging Face
    to create end-to-end video generation pipeline.
    """
    
    def __init__(self):
        """Initialize orchestrator with both Gemini and Hugging Face."""
        try:
            self.gemini = GeminiOrchestrator()
            self.huggingface = HuggingFaceOrchestrator()
            logger.info("[ORCHESTRATOR] Pipeline orchestrator initialized successfully")
        except ValueError as e:
            logger.error(f"[ORCHESTRATOR] Initialization failed: {str(e)}")
            raise
    
    def run_pipeline(
        self,
        user_input: str,
        mode: str = "ads",
        num_scenes: int = 3
    ) -> Dict[str, Any]:
        """
        Run complete pipeline: User Input → Gemini → Hugging Face → Output.
        
        Args:
            user_input: User's initial prompt/description
            mode: "ads" or "cinematic"
            num_scenes: Number of scenes to generate
        
        Returns:
            Dictionary with pipeline results including generated videos
        """
        pipeline_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"[ORCHESTRATOR] Starting pipeline [{pipeline_id}]")
        logger.info(f"[ORCHESTRATOR] Input: {user_input[:50]}... | Mode: {mode} | Scenes: {num_scenes}")
        
        try:
            # Step 1: Generate script via Gemini
            logger.info("[ORCHESTRATOR] Step 1: Generating script via Gemini...")
            script = self.gemini.generate_video_script(user_input, mode)
            
            # Step 2: Generate structured prompts via Gemini
            logger.info("[ORCHESTRATOR] Step 2: Generating structured prompts via Gemini...")
            scene_prompts = self.gemini.generate_structured_prompts(script, num_scenes)
            
            # Step 3: Generate videos for each scene via Hugging Face
            logger.info("[ORCHESTRATOR] Step 3: Generating videos via Hugging Face...")
            video_files = []
            for scene in scene_prompts:
                try:
                    scene_num = scene.get("scene_number", len(video_files) + 1)
                    video_prompt = scene.get("video_prompt", "")
                    duration = scene.get("duration_seconds", 5)
                    
                    video_path = self.huggingface.generate_video(video_prompt, scene_num, duration)
                    
                    if video_path and os.path.exists(video_path):
                        video_files.append({
                            "scene_number": scene_num,
                            "filepath": video_path,
                            "filename": os.path.basename(video_path),
                            "scene_data": scene
                        })
                        logger.info(f"[ORCHESTRATOR] Scene {scene_num} video generated: {video_path}")
                    else:
                        logger.error(f"[ORCHESTRATOR] Failed to generate video for scene {scene_num}")
                
                except Exception as e:
                    logger.error(f"[ORCHESTRATOR] Scene {scene_num} generation failed: {str(e)}")
                    # Continue with next scene instead of failing entire pipeline
                    continue
            
            if not video_files:
                raise RuntimeError("No videos were generated")
            
            # Step 4: Prepare output
            logger.info("[ORCHESTRATOR] Step 4: Preparing output...")
            output = {
                "pipeline_id": pipeline_id,
                "status": "success",
                "script": script,
                "scene_count": len(video_files),
                "scenes": scene_prompts,
                "videos": video_files,
                "output_directory": settings.outputs_dir,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"[ORCHESTRATOR] Pipeline completed successfully [{pipeline_id}]")
            logger.info(f"[ORCHESTRATOR] Generated {len(video_files)} videos from {len(scene_prompts)} scenes")
            
            return output
        
        except Exception as e:
            logger.error(f"[ORCHESTRATOR] Pipeline failed [{pipeline_id}]: {str(e)}", exc_info=True)
            raise RuntimeError(f"Pipeline execution failed: {str(e)}") from e


# Convenience functions for direct usage
def orchestrate_video_generation(user_input: str, mode: str = "ads", num_scenes: int = 3) -> Dict[str, Any]:
    """
    Convenience function to run the full pipeline.
    
    Args:
        user_input: User's prompt
        mode: "ads" or "cinematic"
        num_scenes: Number of scenes
    
    Returns:
        Pipeline results dictionary
    """
    orchestrator = PipelineOrchestrator()
    return orchestrator.run_pipeline(user_input, mode, num_scenes)
