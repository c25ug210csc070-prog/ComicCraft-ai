from ..schemas import PromptRequest
from .gemini_flash import GeminiFlashService
from .gemini_pro import GeminiStoryService
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf


def generate_comic(request: PromptRequest) -> tuple[list[dict], str]:
    outline = GeminiFlashService().generate_outline(request)
    story = GeminiStoryService().generate_story(request, outline)
    image_paths = [generate_image(p.image_prompt, p.panel_number) for p in outline.panels]
    layout = build_comic_layout(outline, story, image_paths)
    pdf_path = save_pdf(layout, title=f"{request.character_name}'s Comic")
    return layout, pdf_path
