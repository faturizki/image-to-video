# 🎬 AI Video Generator (Personal Use)

Sistem AI untuk membuat video iklan / cinematic secara otomatis (durasi 2–5 menit) dengan kontrol penuh dari user.

Fokus:
- Konsistensi karakter
- Scene-based generation
- Kontrol prompt
- Full pipeline otomatis
- Gratis (dengan limit platform)

---

# 🧠 Arsitektur Sistem

Frontend (Vercel) ↓ API Backend (Hugging Face / FastAPI) ↓ AI Pipeline ├── Script Generator ├── Scene Splitter ├── Image/Video Generator ├── Voice Generator (optional) └── Video Merger (FFmpeg) ↓ Output Video

---

# ⚙️ Tech Stack

- Frontend: Next.js (deploy ke Vercel)
- Backend: FastAPI / Hugging Face Spaces
- AI: Hugging Face Models
- Video Processing: FFmpeg
- Storage: Local / Cloud (opsional)
- Version Control: GitHub

---

# 📁 Struktur Project

root/ │ ├── frontend/                 # Dashboard UI (Vercel) │   ├── pages/ │   ├── components/ │   ├── styles/ │   └── utils/ │ ├── backend/                  # AI Engine (Hugging Face) │   ├── app.py │   ├── config.py │   ├── pipeline/ │   │   ├── script_generator.py │   │   ├── scene_splitter.py │   │   ├── prompt_engine.py │   │   ├── image_generator.py │   │   ├── video_generator.py │   │   └── merger.py │ ├── assets/                   # reference images ├── outputs/                  # hasil video ├── requirements.txt └── README.md

---

# 🚀 Setup Project

## 1. API Keys Setup

### For Local Development
1. Copy `.env.example` to `.env`
2. Fill in your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

### For GitHub Actions / Production
1. Go to GitHub → Settings → Secrets and Variables → Actions
2. Add the following secrets:
   - `HUGGINGFACE_API_KEY`: Your Hugging Face API key
   - `OPENAI_API_KEY`: Your OpenAI API key (optional, for script generation)
   - `GEMINI_API_KEY`: Your Google Gemini API key (for script generation)

### Required API Keys
- **Hugging Face API Key**: For image/video generation
- **Gemini API Key**: For script generation with Google Generative AI
- **OpenAI API Key**: (Deprecated, no longer used)

## Testing API Keys

### Validate All API Keys
Before running the application, validate that all API keys are properly configured:

```bash
cd backend
python test_api_keys.py
```

This will test:
- ✓ API key loading from environment
- ✓ API authentication
- ✓ Basic API functionality

**Output Example:**
```
✓ GEMINI: SUCCESS
  Message: API key is valid and working
✓ HUGGINGFACE: SUCCESS
  Message: API key is valid and working
```

### Interactive Test Runner
For a guided testing experience:
```bash
cd backend
bash run_api_tests.sh
```

This provides options to:
1. Test without keys (mock mode)
2. Test with environment variables
3. Test with .env file
4. Run all tests

### Usage with Different Environment Setups

**Local Development (with .env file):**
```bash
cp .env.example .env
# Edit .env with your actual API keys
cd backend
python test_api_keys.py
```

**Using Environment Variables:**
```bash
export GEMINI_API_KEY=your-key-here
export HUGGINGFACE_API_KEY=your-key-here
cd backend
python test_api_keys.py
```

**GitHub Actions:**
API keys are automatically tested during CI/CD pipeline via GitHub Secrets.

See [backend/test_api_keys_README.md](backend/test_api_keys_README.md) for detailed testing documentation.

## Pipeline Orchestrator

The Backend now includes a powerful **Pipeline Orchestrator** that seamlessly integrates Gemini and Hugging Face for end-to-end video generation.

### Quick Start

```python
from pipeline.orchestrator import orchestrate_video_generation

# Generate video with one line
result = orchestrate_video_generation(
    user_input="Create a cinematic video of sunset over ocean",
    mode="cinematic",
    num_scenes=3
)

# Access results
for video in result['videos']:
    print(f"Scene {video['scene_number']}: {video['filename']}")
```

### Orchestrator Flow

```
User Input
    ↓
[Gemini] Generate Script
    ↓
[Gemini] Generate Video Prompts (JSON)
    ↓
[Hugging Face] Generate Videos
    ↓
Output Videos
```

### Usage

**Option 1: Quick One-Liner**
```bash
cd backend
python -c "
from pipeline.orchestrator import orchestrate_video_generation
result = orchestrate_video_generation('Your prompt')
print(f'Generated {result[\"scene_count\"]} videos')
"
```

**Option 2: Full Control**
```python
from pipeline.orchestrator import PipelineOrchestrator

orchestrator = PipelineOrchestrator()
result = orchestrator.run_pipeline(
    user_input="Product advertisement",
    mode="ads",
    num_scenes=5
)
```

**Option 3: Component Testing**
```python
from pipeline.orchestrator import GeminiOrchestrator, HuggingFaceOrchestrator

# Test Gemini separately
gemini = GeminiOrchestrator()
script = gemini.generate_video_script("Your prompt", mode="ads")
prompts = gemini.generate_structured_prompts(script, num_scenes=3)

# Test Hugging Face separately
hf = HuggingFaceOrchestrator()
if hf.validate_api_key():
    video = hf.generate_video("Video description", scene_num=1)
```

### Output Format

```json
{
  "pipeline_id": "20260402_150234",
  "status": "success",
  "script": "Generated narrative script...",
  "scene_count": 3,
  "scenes": [
    {
      "scene_number": 1,
      "scene_description": "Scene description",
      "video_prompt": "Detailed video generation prompt",
      "duration_seconds": 5,
      "visual_style": "cinematic"
    }
  ],
  "videos": [
    {
      "scene_number": 1,
      "filepath": "/path/to/video.mp4",
      "filename": "video_scene_1.mp4"
    }
  ]
}
```

For detailed documentation, see [backend/ORCHESTRATOR_GUIDE.md](backend/ORCHESTRATOR_GUIDE.md)

## 2. Install Dependencies

### Backend
```bash
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## 2. Run Backend
```bash
cd backend
python -m backend.app
```
Server akan berjalan di http://localhost:8000

## 3. Run Frontend
```bash
cd frontend
npm run dev
```
Frontend akan berjalan di http://localhost:3000

## 4. Test
Buka http://localhost:3000, isi form, dan generate video.

---

# 📁 Struktur Project

root/
│
├── frontend/ (Next.js)
│   ├── pages/
│   │   ├── index.js          # Dashboard UI
│   │   └── _app.js
│   ├── components/
│   ├── services/api.js       # API client
│   ├── hooks/
│   └── styles/
│       └── globals.css
│
├── backend/ (FastAPI)
│   ├── app.py                 # Main FastAPI app
│   ├── config.py              # Settings
│   ├── pipeline/
│   │   ├── run_pipeline.py    # Main pipeline
│   │   ├── script_generator.py
│   │   ├── scene_splitter.py
│   │   ├── prompt_engine.py
│   │   ├── image_generator.py
│   │   ├── video_generator.py
│   │   └── merger.py
│   └── utils/
│
├── assets/
├── outputs/
├── requirements.txt
└── README.md
pip install -r requirements.txt


---

3. Install Frontend Dependencies

cd frontend
npm install


---

▶️ Menjalankan Project

Backend (AI Engine)

cd backend
uvicorn app:app --host 0.0.0.0 --port 8000


---

Frontend (Dashboard)

cd frontend
npm run dev

Akses:

http://localhost:3000


---

🌐 Deployment

Frontend → Vercel

1. Push ke GitHub


2. Masuk ke: 👉 https://vercel.com


3. Import project


4. Klik Deploy




---

Backend → Hugging Face

1. Masuk: 👉 https://huggingface.co/spaces


2. Buat Space baru


3. Upload backend


4. Pilih:

FastAPI / Gradio



5. Jalankan




---

🔗 Integrasi Frontend → Backend

const generateVideo = async () => {
  const response = await fetch("https://your-space.hf.space/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      prompt: "luxury eyelash commercial",
      mode: "cinematic",
      duration: "3 minutes"
    })
  });

  const data = await response.json();
  return data;
};


---

🎬 Pipeline AI (Inti Sistem)

1. User input prompt
2. Generate script (AI)
3. Split menjadi scene:
   - Scene 1 (Hook)
   - Scene 2 (Problem)
   - Scene 3 (Solution)
   - Scene 4 (CTA)
4. Generate visual per scene
5. (Optional) Generate voice
6. Merge video (FFmpeg)
7. Output final video


---

🧩 Scene System

Gunakan struktur scene untuk menjaga konsistensi:

[
  "Scene 1: cinematic close-up eyes, dramatic lighting",
  "Scene 2: product reveal",
  "Scene 3: transformation effect",
  "Scene 4: branding + CTA"
]


---

🎯 Prompt Template

Gunakan prompt konsisten:

same character, consistent identity,
luxury cinematic lighting, ultra realistic,
high detail, 4k, smooth motion,
commercial quality


---

🎥 Video Output

Disimpan di:

/outputs/final_video.mp4


---

🔊 Voice (Optional)

ElevenLabs

Coqui TTS


Output:

voice.mp3


---

⚠️ Limitasi

Hugging Face Free:

GPU terbatas

Queue processing

Latency


Vercel:

hanya frontend

tidak untuk AI berat



---

💡 Best Practice

Gunakan scene pendek

Gunakan reference image untuk karakter

Gunakan prompt konsisten

Hindari terlalu banyak variasi

Simpan hasil per scene



---

🧠 Tips Konsistensi

Gunakan:

seed tetap

reference image

prompt yang sama

LoRA (advanced)



---

📦 Output Pipeline

INPUT → SCRIPT → SCENE → GENERATE → MERGE → OUTPUT


---

🔥 Roadmap

[ ] Auto scene optimization

[ ] Character consistency (LoRA)

[ ] Voice sync

[ ] Multi-language

[ ] Template ads system

[ ] Monetization tools



---

🤝 Penggunaan

Sistem ini untuk:

penggunaan pribadi

eksperimen AI

pembelajaran



---

📄 License

MIT License


---

🚀 Goal

Membangun AI yang:

otomatis membuat video

konsisten karakter

bisa dikontrol user

scalable

siap dikembangkan
