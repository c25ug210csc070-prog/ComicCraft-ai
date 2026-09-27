# ComicCraft - AI Comic Story Creator

ComicCraft is a FastAPI web application that turns a user's story prompt into a five-panel comic. It follows the architecture described in the supplied project documentation: Jinja2 frontend, FastAPI backend, Gemini-based outline/story generation, AI image generation, panel layout assembly, and PDF export.

## Current implementation note

The supplied document names `gemini-1.5-flash`, `gemini-1.5-pro`, and `runwayml/stable-diffusion-v1-5`. Those model choices are historical. This implementation keeps the same logical roles but makes model IDs configurable through `.env`. The defaults use currently documented Gemini models and Hugging Face Inference Providers so the project is practical on a normal development laptop.

Image generation defaults to Hugging Face's hosted inference path. A local Diffusers/Stable Diffusion path is also included and can be enabled with `IMAGE_PROVIDER=local`.

## Architecture

- `app/main.py` - FastAPI application and static-file mounting.
- `app/routes.py` - browser and JSON API routes.
- `app/schemas.py` - Pydantic request/response models.
- `app/services/gemini_flash.py` - structured comic outline generation.
- `app/services/gemini_pro.py` - detailed narration/dialogue generation.
- `app/services/image_generator.py` - Hugging Face or local Diffusers image generation.
- `app/services/layout_builder.py` - combines story and images.
- `app/services/exporters.py` - PDF export.
- `app/services/workflow.py` - end-to-end orchestration.
- `app/templates/` - Jinja2 pages.
- `app/static/` - CSS and JavaScript.
- `static/panels/` - generated panel images.
- `static/exports/` - generated PDFs.
- `tests/` - smoke tests that do not call external AI APIs.

## Setup in VS Code on Windows

1. Install Python 3.11+ and Git.
2. Open this folder in VS Code.
3. Create an environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env`.
5. Add your Gemini API key and Hugging Face token.
6. Keep `IMAGE_PROVIDER=hf` for the easiest setup.
7. Start the server:

```powershell
uvicorn app.main:app --reload
```

8. Open `http://127.0.0.1:8000`.
9. API docs: `http://127.0.0.1:8000/docs`.

## API example

POST `/generate-comic/json` with:

```json
{
  "story_prompt": "A brave fox explores an enchanted forest and discovers a forgotten library.",
  "character_name": "Luna",
  "setting": "Forest",
  "tone": "Adventure",
  "art_style": "Comic book"
}
```

## Test without calling AI

```powershell
pytest -q
```

## Local Stable Diffusion option

Install the optional packages:

```powershell
pip install -r requirements-local-diffusion.txt
```

Then set in `.env`:

```text
IMAGE_PROVIDER=local
LOCAL_IMAGE_MODEL=runwayml/stable-diffusion-v1-5
```

A CUDA-capable GPU is strongly recommended. Local model downloads are large and generation is much slower on CPU.

## Troubleshooting

- `GEMINI_API_KEY is not configured`: add a valid Gemini API key to `.env`.
- `HF_TOKEN is required`: add a Hugging Face token with inference permissions, or switch to `IMAGE_PROVIDER=local`.
- Image provider/model unavailable: choose an image model currently offered by a Hugging Face Inference Provider and update `HF_IMAGE_MODEL`.
- PDF font issues: the exporter automatically looks for common DejaVu/Liberation/Windows fonts and falls back to Helvetica.
- PowerShell activation blocked: run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal only, then activate the environment.
