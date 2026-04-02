#!/usr/bin/env python3
"""
End-to-End Orchestrator Demo

This script demonstrates the complete orchestrator pipeline flow:
1. Initialize orchestrator with API key validation
2. Generate script via Gemini
3. Generate structured prompts
4. Generate videos via Hugging Face
5. Return complete results

Run with: python orchestrator_demo.py
"""

import sys
import os
import json
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.orchestrator import (
    GeminiOrchestrator,
    HuggingFaceOrchestrator,
    PipelineOrchestrator,
    orchestrate_video_generation
)

# Configure logging with better formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def print_section(title):
    """Print formatted section header."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def demo_orchestrator_components():
    """
    Demonstrate individual orchestrator components and their capabilities.
    """
    print_section("DEMO 1: Orchestrator Component Architecture")
    
    print("✓ Available Components:")
    print("  1. GeminiOrchestrator - Script and prompt generation")
    print("  2. HuggingFaceOrchestrator - Video generation")
    print("  3. PipelineOrchestrator - Full pipeline coordination")
    print("  4. orchestrate_video_generation() - Convenience function")
    
    print("\n✓ Component Methods:")
    print("\n  GeminiOrchestrator:")
    print("    - generate_video_script(prompt, mode) → str")
    print("    - generate_structured_prompts(script, num_scenes) → List[Dict]")
    
    print("\n  HuggingFaceOrchestrator:")
    print("    - validate_api_key() → bool")
    print("    - generate_video(prompt, scene_num, duration) → str")
    
    print("\n  PipelineOrchestrator:")
    print("    - run_pipeline(user_input, mode, num_scenes) → Dict")


def demo_pipeline_flow():
    """
    Demonstrate the pipeline data flow with mock data.
    """
    print_section("DEMO 2: Pipeline Data Flow")
    
    mock_user_input = "Create a product demo video for a new mobile app"
    
    print(f"Input: {mock_user_input}\n")
    
    print("STEP 1: Generate Script (Gemini)")
    print("-" * 80)
    mock_script = """Opening: Sleek mobile app interface appears on screen.
Features: App shows key features - smooth animations, intuitive UI.
Demo: User interactions demonstrating main functionality.
Call-to-Action: Download button with engagement reminder.
Closing: App logo and website URL."""
    print(mock_script)
    
    print("\n\nSTEP 2: Parse into Structured Prompts (Gemini → JSON)")
    print("-" * 80)
    mock_prompts = [
        {
            "scene_number": 1,
            "scene_description": "App opening screen",
            "video_prompt": "Modern mobile app launching, smooth entrance animation, glass morphism UI, soft blue lighting",
            "duration_seconds": 5,
            "visual_style": "cinematic"
        },
        {
            "scene_number": 2,
            "scene_description": "Feature showcase",
            "video_prompt": "Close-up of app features, smooth transitions between screens, UI elements highlighted",
            "duration_seconds": 5,
            "visual_style": "cinematic"
        },
        {
            "scene_number": 3,
            "scene_description": "Call to action",
            "video_prompt": "Download button prominent, app store badges, professional overlay, motion graphics",
            "duration_seconds": 4,
            "visual_style": "cinematic"
        }
    ]
    print(json.dumps(mock_prompts, indent=2))
    
    print("\n\nSTEP 3: Generate Videos (Hugging Face)")
    print("-" * 80)
    for prompt in mock_prompts:
        print(f"Scene {prompt['scene_number']}: {prompt['scene_description']}")
        print(f"  Prompt: {prompt['video_prompt'][:70]}...")
        print(f"  Duration: {prompt['duration_seconds']}s")
        print(f"  Status: ✓ Generated → video_scene_{prompt['scene_number']}.mp4")
    
    print("\n\nFINAL OUTPUT")
    print("-" * 80)
    mock_result = {
        "pipeline_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "status": "success",
        "script": mock_script,
        "scene_count": 3,
        "scenes": mock_prompts,
        "videos": [
            {"scene_number": i+1, "filename": f"video_scene_{i+1}.mp4"}
            for i in range(len(mock_prompts))
        ],
        "generated_at": datetime.now().isoformat()
    }
    print(json.dumps(mock_result, indent=2))


def demo_error_handling():
    """
    Demonstrate error handling and graceful degradation.
    """
    print_section("DEMO 3: Error Handling and Robustness")
    
    print("✓ Error Handling Features:")
    print("  1. Missing API Keys")
    print("     - Raises ValueError with clear message")
    print("     - Prevents initialization without credentials")
    print("     - Guides user to configure keys")
    
    print("\n  2. Invalid Prompts")
    print("     - Validates input non-empty")
    print("     - Validates mode is 'ads' or 'cinematic'")
    print("     - Raises ValueError with helpful message")
    
    print("\n  3. API Failures")
    print("     - Catches exceptions from API calls")
    print("     - Falls back to mock generation for testing")
    print("     - Logs detailed error information")
    print("     - Continues with remaining scenes")
    
    print("\n  4. Partial Failures")
    print("     - If scene 2 fails, scenes 1 and 3 still complete")
    print("     - Returns partial result with available videos")
    print("     - Includes error details in logs")
    
    print("\n✓ API Key Validation")
    print("  - GeminiOrchestrator validates GEMINI_API_KEY")
    print("  - HuggingFaceOrchestrator validates HUGGINGFACE_API_KEY")
    print("  - PipelineOrchestrator validates both")
    print("  - HuggingFace.validate_api_key() tests authentication")


def demo_integration_points():
    """
    Demonstrate how to integrate orchestrator with existing systems.
    """
    print_section("DEMO 4: Integration Points")
    
    print("✓ Option 1: Direct Usage in FastAPI")
    print("""
    @app.post("/generate-v2")
    async def generate_video_v2(request: GenerateRequest):
        from pipeline.orchestrator import orchestrate_video_generation
        
        result = orchestrate_video_generation(
            user_input=request.prompt,
            mode=request.mode,
            num_scenes=3
        )
        return result
    """)
    
    print("\n✓ Option 2: Replace existing run_pipeline")
    print("""
    # Old way:
    # result = await run_pipeline(prompt, mode, duration, reference_image)
    
    # New way:
    from pipeline.orchestrator import PipelineOrchestrator
    orchestrator = PipelineOrchestrator()
    result = orchestrator.run_pipeline(prompt, mode, num_scenes=5)
    """)
    
    print("\n✓ Option 3: Async Integration")
    print("""
    import asyncio
    from pipeline.orchestrator import orchestrate_video_generation
    
    async def generate_videos_async(prompts):
        tasks = [
            asyncio.to_thread(
                orchestrate_video_generation,
                prompt,
                mode="ads",
                num_scenes=3
            )
            for prompt in prompts
        ]
        return await asyncio.gather(*tasks)
    """)
    
    print("\n✓ Option 4: Webhook/Queue Integration")
    print("""
    # Enqueue orchestrator job
    job_id = task_queue.enqueue(
        orchestrate_video_generation,
        user_input="Your prompt",
        mode="cinematic",
        num_scenes=5
    )
    
    # Retrieve results later
    result = task_queue.get_result(job_id)
    """)


def demo_advanced_usage():
    """
    Demonstrate advanced usage patterns.
    """
    print_section("DEMO 5: Advanced Usage Patterns")
    
    print("✓ Pattern 1: Batch Processing")
    print("""
    prompts = [
        "Generate commercial #1",
        "Generate commercial #2",
        "Generate commercial #3"
    ]
    
    from pipeline.orchestrator import orchestrate_video_generation
    
    results = []
    for prompt in prompts:
        result = orchestrate_video_generation(prompt, mode="ads", num_scenes=3)
        results.append(result)
        print(f"Generated {result['scene_count']} videos")
    """)
    
    print("\n✓ Pattern 2: Custom Pipeline Workflow")
    print("""
    from pipeline.orchestrator import GeminiOrchestrator, HuggingFaceOrchestrator
    
    gemini = GeminiOrchestrator()
    hf = HuggingFaceOrchestrator()
    
    # Generate multiple scripts
    scripts = [
        gemini.generate_video_script(f"Topic {i}", mode="ads")
        for i in range(3)
    ]
    
    # Process each script
    all_videos = []
    for script in scripts:
        prompts = gemini.generate_structured_prompts(script, num_scenes=2)
        for prompt in prompts:
            video = hf.generate_video(prompt['video_prompt'], prompt['scene_number'])
            all_videos.append(video)
    """)
    
    print("\n✓ Pattern 3: Result Caching")
    print("""
    import pickle
    
    result = orchestrate_video_generation("prompt", "ads", 3)
    
    # Save result
    with open('result_cache.pkl', 'wb') as f:
        pickle.dump(result, f)
    
    # Load later
    with open('result_cache.pkl', 'rb') as f:
        cached_result = pickle.load(f)
    """)
    
    print("\n✓ Pattern 4: Progress Monitoring")
    print("""
    from pipeline.orchestrator import PipelineOrchestrator
    import logging
    
    # Enable detailed logging
    logging.basicConfig(level=logging.DEBUG)
    
    orchestrator = PipelineOrchestrator()
    
    # Monitor progress in logs
    result = orchestrator.run_pipeline(
        user_input="prompt",
        mode="cinematic",
        num_scenes=5
    )
    
    # [ORCHESTRATOR] Step 1: Generating script...
    # [GEMINI] Generating cinematic script...
    # [ORCHESTRATOR] Step 2: Generating prompts...
    # [ORCHESTRATOR] Step 3: Generating videos...
    # [HUGGINGFACE] Generating video for scene 1...
    """)


def print_quickstart():
    """
    Print quick start instructions.
    """
    print_section("QUICK START")
    
    print("1. Ensure API keys are configured:")
    print("   export GEMINI_API_KEY=your-key-here")
    print("   export HUGGINGFACE_API_KEY=your-key-here")
    
    print("\n2. Use orchestrator in your code:")
    print("   from pipeline.orchestrator import orchestrate_video_generation")
    print("   result = orchestrate_video_generation('Your prompt')")
    
    print("\n3. Access results:")
    print("   print(f'Generated {result[\"scene_count\"]} videos')")
    print("   for video in result['videos']:")
    print("       print(video['filename'])")
    
    print("\n4. Check detailed documentation:")
    print("   - ORCHESTRATOR_GUIDE.md - Complete API reference")
    print("   - test_orchestrator.py - Test suite")
    print("   - This script - Architecture and patterns")


def main():
    """
    Run all demos.
    """
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "PIPELINE ORCHESTRATOR - FULL DEMONSTRATION" + " " * 17 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        demo_orchestrator_components()
        demo_pipeline_flow()
        demo_error_handling()
        demo_integration_points()
        demo_advanced_usage()
        print_quickstart()
        
        print("\n" + "=" * 80)
        print("✓ Demonstration Complete!")
        print("=" * 80)
        print("\nFor production use:")
        print("1. Set real API keys")
        print("2. Test with test_orchestrator.py")
        print("3. Review ORCHESTRATOR_GUIDE.md")
        print("4. Integrate into your application")
        print("\n")
    
    except Exception as e:
        logger.error(f"Demo error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
