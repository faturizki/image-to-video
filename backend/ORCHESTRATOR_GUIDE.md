"""
Pipeline Orchestrator - Complete Documentation

The Pipeline Orchestrator is the core system that coordinates AI model integration between
Gemini and Hugging Face for end-to-end video generation.

## Architecture

         User Input
            ↓
    ┌──────────────┐
    │   Orchestrator
    └──────────────┘
         ↓      ↓
      GEMINI   HUGGING FACE
         │      │
         ├─────┬┘
         ↓     ↓
    Script   Videos
         ↓
      Output


## Components

### 1. GeminiOrchestrator
Handles all Gemini API interactions:
- generate_video_script(): Creates narrative scripts from prompts
- generate_structured_prompts(): Parses scripts into structured video prompts (JSON)

### 2. HuggingFaceOrchestrator
Handles all Hugging Face API interactions:
- validate_api_key(): Checks API credentials
- generate_video(): Generates videos from prompts

### 3. PipelineOrchestrator
Main orchestrator that:
- Initializes both Gemini and Hugging Face orchestrators
- Runs complete pipeline: input → script → prompts → videos → output
- Handles error recovery and logging
- Manages pipeline metadata and results

## Quick Start

### Basic Usage

```python
from pipeline.orchestrator import orchestrate_video_generation

# Simple one-liner for video generation
result = orchestrate_video_generation(
    user_input="Create a cinematic video of sunset over ocean",
    mode="cinematic",
    num_scenes=3
)

print(f"Generated {result['scene_count']} videos")
for video in result['videos']:
    print(f"  Scene {video['scene_number']}: {video['filename']}")
```

### Advanced Usage

```python
from pipeline.orchestrator import PipelineOrchestrator

# Full orchestrator with fine-grained control
orchestrator = PipelineOrchestrator()

# Run pipeline
result = orchestrator.run_pipeline(
    user_input="Product advertisement video",
    mode="ads",
    num_scenes=5
)

# Access results
print(f"Pipeline ID: {result['pipeline_id']}")
print(f"Status: {result['status']}")
print(f"Script: {result['script']}")
print(f"Videos generated: {len(result['videos'])}")

# Save results to file
import json
with open('pipeline_result.json', 'w') as f:
    json.dump(result, f, indent=2)
```

### Component-Level Usage

```python
from pipeline.orchestrator import GeminiOrchestrator, HuggingFaceOrchestrator

# Use Gemini separately
gemini = GeminiOrchestrator()
script = gemini.generate_video_script("Your prompt", mode="ads")
scenes = gemini.generate_structured_prompts(script, num_scenes=4)

# Use Hugging Face separately
hf = HuggingFaceOrchestrator()
if hf.validate_api_key():
    for scene in scenes:
        video = hf.generate_video(scene['video_prompt'], scene['scene_number'])
```

## API Reference

### PipelineOrchestrator

#### `__init__()`
Initialize orchestrator with Gemini and Hugging Face.

**Raises:**
- ValueError: If GEMINI_API_KEY or HUGGINGFACE_API_KEY not configured

**Example:**
```python
orchestrator = PipelineOrchestrator()
```

#### `run_pipeline(user_input, mode="ads", num_scenes=3) → Dict`
Execute complete pipeline.

**Parameters:**
- user_input (str): User's initial prompt
- mode (str): "ads" or "cinematic"
- num_scenes (int): Number of scenes to generate (default: 3)

**Returns:**
```python
{
    "pipeline_id": "20260402_150234",
    "status": "success",
    "script": "Generated script...",
    "scene_count": 3,
    "scenes": [
        {
            "scene_number": 1,
            "scene_description": "...",
            "video_prompt": "...",
            "duration_seconds": 5,
            "visual_style": "cinematic"
        },
        ...
    ],
    "videos": [
        {
            "scene_number": 1,
            "filepath": "/path/to/video.mp4",
            "filename": "video_scene_1.mp4",
            "scene_data": {...}
        },
        ...
    ],
    "output_directory": "/outputs",
    "generated_at": "2026-04-02T15:02:34.123456"
}
```

**Raises:**
- RuntimeError: If pipeline execution fails
- ValueError: If required API keys missing

### GeminiOrchestrator

#### `generate_video_script(user_input, mode="ads") → str`
Generate narrative script.

**Parameters:**
- user_input (str): User prompt
- mode (str): "ads" or "cinematic"

**Returns:** Script as string

#### `generate_structured_prompts(script, num_scenes=3) → List[Dict]`
Parse script into structured scene prompts.

**Parameters:**
- script (str): Generated script
- num_scenes (int): Number of scenes

**Returns:** List of scene dictionaries with video prompts

### HuggingFaceOrchestrator

#### `validate_api_key() → bool`
Test API key validity.

**Returns:** True if valid, False otherwise

#### `generate_video(prompt, scene_num, duration=5) → str`
Generate video for a scene.

**Parameters:**
- prompt (str): Video description
- scene_num (int): Scene number
- duration (int): Duration in seconds

**Returns:** Path to generated video file

## Configuration

### Environment Variables

```bash
# Required
export GEMINI_API_KEY="your-gemini-api-key"
export HUGGINGFACE_API_KEY="your-huggingface-api-key"
```

### .env File

```
GEMINI_API_KEY=your-gemini-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key
```

### GitHub Actions

Set these as repository secrets:
1. Go to: Settings → Secrets and variables → Actions
2. Add:
   - GEMINI_API_KEY
   - HUGGINGFACE_API_KEY

## Structured Prompt Format

Gemini generates structured prompts in JSON format:

```json
[
    {
        "scene_number": 1,
        "scene_description": "Product introduction in modern setting",
        "video_prompt": "A sleek smartphone being displayed on a reflection, with soft lighting, professional product photography style, 4K",
        "duration_seconds": 5,
        "visual_style": "cinematic"
    },
    {
        "scene_number": 2,
        "scene_description": "Features showcase",
        "video_prompt": "Close-up of smartphone features, UI elements, smooth transitions, blue accent lighting",
        "duration_seconds": 5,
        "visual_style": "cinematic"
    }
]
```

## Error Handling

### Missing API Keys
```python
try:
    orchestrator = PipelineOrchestrator()
except ValueError as e:
    print(f"Configuration error: {e}")
    # Handle missing API keys
```

### Pipeline Failures
```python
try:
    result = orchestrator.run_pipeline("prompt", mode="ads", num_scenes=3)
except RuntimeError as e:
    print(f"Pipeline failed: {e}")
    # Handle failure
```

### Partial Success
- If some scenes fail to generate, pipeline continues with remaining scenes
- Check `result['scene_count']` vs `result['videos']` length
- Partial results are returned with success status and available videos

## Logging

Orchestrator logs all operations with `[ORCHESTRATOR]` prefix:

```
[ORCHESTRATOR] Pipeline orchestrator initialized successfully
[ORCHESTRATOR] Starting pipeline [20260402_150234]
[ORCHESTRATOR] Step 1: Generating script via Gemini...
[GEMINI] Generating ads script for: Create a cinematic video...
[ORCHETSRATOR] Step 2: Generating structured prompts via Gemini...
[HUGGINGFACE] Generating video for scene 1: A sleek smartphone...
[ORCHESTRATOR] Pipeline completed successfully [20260402_150234]
```

## Testing

Run the test suite:

```bash
cd backend
python test_orchestrator.py
```

This validates:
- Orchestrator structure and methods
- Convenience functions
- Error handling with missing keys
- Environment variable configuration

## Performance Notes

- Script generation: ~2-5 seconds (Gemini API)
- Prompt generation: ~1-2 seconds (Gemini API)
- Video generation: ~5-30 seconds per scene (Hugging Face API)
- Total pipeline: ~30 seconds - 3 minutes (depending on scene count and API service)

## Integration with Existing Pipeline

The orchestrator can be used standalone or integrated with run_pipeline:

```python
# Option 1: Use orchestrator directly for new pipeline version
from pipeline.orchestrator import orchestrate_video_generation
result = orchestrate_video_generation(prompt, mode, num_scenes)

# Option 2: Use existing run_pipeline (calls individual components)
from pipeline.run_pipeline import run_pipeline
result = await run_pipeline(prompt, mode, duration, reference_image)

# Option 3: Mix both - use orchestrator for script/prompts, then continue
# with existing pipeline for merger and other steps
```

## Future Enhancements

- Caching for duplicate prompts
- Batch processing multiple user inputs
- Custom model selection
- Advanced prompt optimization
- Video post-processing effects
- Real-time progress callbacks
- Webhook integration for async processing
"""
