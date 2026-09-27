from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..config import get_settings
from .schemas import PromptRequest
from .services.workflow import generate_comic
from .services.image_generator import generate_image

router = APIRouter()
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        payload = PromptRequest(story_prompt=story_prompt, character_name=character_name, setting=setting, tone=tone, art_style=art_style)
        layout, pdf_path = generate_comic(payload)
        return templates.TemplateResponse("comic_preview.html", {"request": request, "layout": layout, "pdf_path": pdf_path, "character_name": payload.character_name})
    except Exception as exc:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(exc)}, status_code=500)

@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):
    try:
        layout, pdf_path = generate_comic(payload)
        return {"success": True, "layout": layout, "pdf_path": pdf_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str = "/"):
    return templates.TemplateResponse("export_success.html", {"request": request, "pdf_path": pdf_path})

@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    try:
        return {"success": True, "image_path": generate_image(prompt, 0)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.get("/health")
async def health():
    return {"status": "ok", "image_provider": settings.image_provider, "outline_model": settings.gemini_outline_model, "story_model": settings.gemini_story_model}
