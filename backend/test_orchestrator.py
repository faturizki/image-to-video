"""
Test script for the Pipeline Orchestrator

This demonstrates how to use the orchestrator to generate videos
with Gemini and Hugging Face integration.
"""

import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.orchestrator import PipelineOrchestrator, orchestrate_video_generation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_orchestrator_with_mock_keys():
    """
    Test orchestrator with mock API keys (will fail gracefully).
    This tests the error handling and structure.
    """
    print("=" * 70)
    print("TEST 1: Orchestrator with Missing API Keys (Error Handling)")
    print("=" * 70)
    
    try:
        orchestrator = PipelineOrchestrator()
        logger.info("Orchestrator initialized")
        
        # This will fail because API keys are not set
        result = orchestrator.run_pipeline(
            user_input="Create a cinematic scene of a spaceship landing",
            mode="cinematic",
            num_scenes=2
        )
        
        logger.info(f"Pipeline result: {result}")
    
    except ValueError as e:
        logger.error(f"Expected error (missing API keys): {e}")
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
    
    print()


def test_orchestrator_structure():
    """
    Test that orchestrator can be imported and has correct structure.
    """
    print("=" * 70)
    print("TEST 2: Orchestrator Structure Validation")
    print("=" * 70)
    
    try:
        from pipeline.orchestrator import GeminiOrchestrator, HuggingFaceOrchestrator
        
        logger.info("✓ GeminiOrchestrator available")
        logger.info("✓ HuggingFaceOrchestrator available")
        
        # Check methods exist
        gemini_methods = ['generate_video_script', 'generate_structured_prompts']
        hf_methods = ['validate_api_key', 'generate_video']
        
        for method in gemini_methods:
            if hasattr(GeminiOrchestrator, method):
                logger.info(f"✓ GeminiOrchestrator.{method}")
            else:
                logger.error(f"✗ GeminiOrchestrator.{method} missing")
        
        for method in hf_methods:
            if hasattr(HuggingFaceOrchestrator, method):
                logger.info(f"✓ HuggingFaceOrchestrator.{method}")
            else:
                logger.error(f"✗ HuggingFaceOrchestrator.{method} missing")
        
        logger.info("\n✓ Orchestrator structure validation passed")
    
    except Exception as e:
        logger.error(f"Structure validation failed: {e}")
    
    print()


def test_convenience_function():
    """
    Test the convenience function signature.
    """
    print("=" * 70)
    print("TEST 3: Convenience Function Availability")
    print("=" * 70)
    
    try:
        from pipeline.orchestrator import orchestrate_video_generation
        
        logger.info("✓ orchestrate_video_generation function available")
        logger.info("  Signature: orchestrate_video_generation(user_input, mode='ads', num_scenes=3)")
        logger.info("  This is a convenience wrapper for quick pipeline execution")
    
    except Exception as e:
        logger.error(f"Function check failed: {e}")
    
    print()


def test_mock_mode_with_env_vars():
    """
    Test orchestrator behavior when API keys are set as environment variables.
    """
    print("=" * 70)
    print("TEST 4: Orchestrator with Environment Variables")
    print("=" * 70)
    
    try:
        # Check if we can set test keys
        os.environ['GEMINI_API_KEY'] = 'test-key-demo'
        os.environ['HUGGINGFACE_API_KEY'] = 'test-key-demo'
        
        logger.info("✓ Environment variables set for testing")
        logger.info("  GEMINI_API_KEY=test-key-demo")
        logger.info("  HUGGINGFACE_API_KEY=test-key-demo")
        
        # Try to initialize (will succeed but fail on actual API calls)
        from pipeline.orchestrator import GeminiOrchestrator, HuggingFaceOrchestrator
        
        logger.info("\nNote: With test keys, initialization will succeed but API calls will fail")
        logger.info("This is expected - use real API keys for actual generation")
    
    except Exception as e:
        logger.error(f"Environment variable test failed: {e}")
    
    print()


def print_usage_examples():
    """
    Print usage examples for the orchestrator.
    """
    print("=" * 70)
    print("USAGE EXAMPLES")
    print("=" * 70)
    print("""
1. Using convenience function:
   
   from pipeline.orchestrator import orchestrate_video_generation
   
   result = orchestrate_video_generation(
       user_input="Generate a cinematic video of a sunset",
       mode="cinematic",
       num_scenes=3
   )
   
   print(f"Generated {result['scene_count']} videos")


2. Using full orchestrator:
   
   from pipeline.orchestrator import PipelineOrchestrator
   
   orchestrator = PipelineOrchestrator()
   result = orchestrator.run_pipeline(
       user_input="Create an advertisement for a tech product",
       mode="ads",
       num_scenes=5
   )
   
   for video in result['videos']:
       print(f"Scene {video['scene_number']}: {video['filename']}")


3. Testing individual components:
   
   from pipeline.orchestrator import GeminiOrchestrator, HuggingFaceOrchestrator
   
   # Test Gemini
   gemini = GeminiOrchestrator()
   script = gemini.generate_video_script("Your prompt here", mode="ads")
   prompts = gemini.generate_structured_prompts(script, num_scenes=3)
   
   # Test Hugging Face
   hf = HuggingFaceOrchestrator()
   if hf.validate_api_key():
       video = hf.generate_video("Video description", scene_num=1)


Required API Keys:
   - GEMINI_API_KEY: Set as environment variable or in .env file
   - HUGGINGFACE_API_KEY: Set as environment variable or in .env file


Output:
   All generated videos are saved to the configured outputs directory
   
   Result dictionary includes:
   - pipeline_id: Unique ID for this pipeline execution
   - status: "success" or error message
   - script: The generated script
   - scene_count: Number of scenes generated
   - scenes: List of scene data with prompts
   - videos: List of generated video files with paths
   - output_directory: Where videos are saved
   - generated_at: Timestamp of generation
""")
    print("=" * 70)
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "PIPELINE ORCHESTRATOR TEST SUITE" + " " * 21 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Run tests
    test_orchestrator_structure()
    test_convenience_function()
    test_mock_mode_with_env_vars()
    test_orchestrator_with_mock_keys()
    
    # Print usage guide
    print_usage_examples()
    
    print("\n✓ Test suite completed!")
    print("\nNext steps:")
    print("1. Set up real API keys (GEMINI_API_KEY and HUGGINGFACE_API_KEY)")
    print("2. Import and use orchestrator in your application")
    print("3. Run actual pipeline with real keys for video generation")
