from google import genai
from ..config import get_settings
from ..schemas import ComicOutline, ComicStory, PromptRequest

class GeminiStoryService:
    def __init__(self):
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_story_model

    def generate_story(self, request: PromptRequest, outline: ComicOutline) -> ComicStory:
        outline_text = outline.model_dump_json(indent=2)
        prompt = f"""Expand this comic outline into polished comic narration and dialogue.
User concept: {request.story_prompt}
Character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Outline:
{outline_text}

Requirements:
- Preserve the exact panel count and panel numbers.
- Keep plot continuity and character consistency.
- caption: one short atmospheric caption.
- narration: 1-3 concise sentences.
- dialogue: 0-3 short spoken lines, formatted as plain text without speaker labels if possible.
- Do not invent a different setting or protagonist.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ComicStory.model_json_schema(),
            },
        )
        story = ComicStory.model_validate_json(response.text)
        if len(story.panels) != len(outline.panels):
            raise RuntimeError("Story panel count does not match outline")
        return story
