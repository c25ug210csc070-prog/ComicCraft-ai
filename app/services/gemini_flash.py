from google import genai
from ..config import get_settings
from ..schemas import ComicOutline, PromptRequest

class GeminiFlashService:
    def __init__(self):
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_outline_model
        self.panel_count = settings.panels_count

    def generate_outline(self, request: PromptRequest) -> ComicOutline:
        prompt = f"""Create a coherent {self.panel_count}-panel comic outline.
User concept: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Requirements:
- Exactly {self.panel_count} panels, numbered 1 through {self.panel_count}.
- Keep the same main character and visual identity throughout.
- Each panel must advance the story.
- scene_description describes what is happening visually.
- image_prompt is a detailed prompt for a text-to-image model; do not include speech bubbles or written text inside the image.
- Keep image prompts visually consistent and safe.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ComicOutline.model_json_schema(),
            },
        )
        outline = ComicOutline.model_validate_json(response.text)
        if len(outline.panels) != self.panel_count:
            raise RuntimeError(f"Gemini returned {len(outline.panels)} panels; expected {self.panel_count}")
        return outline
