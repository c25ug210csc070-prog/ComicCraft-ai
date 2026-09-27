from pydantic import BaseModel, Field, field_validator
from typing import List

class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=5, max_length=2000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=120)
    tone: str = Field(min_length=1, max_length=80)
    art_style: str = Field(min_length=1, max_length=120)

    @field_validator("story_prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = " ".join(value.strip().split())
        if not value:
            raise ValueError("Value cannot be empty")
        return value

class ComicPanelOutline(BaseModel):
    panel_number: int = Field(ge=1)
    title: str
    scene_description: str
    image_prompt: str

class ComicOutline(BaseModel):
    panels: List[ComicPanelOutline]

class StoryPanel(BaseModel):
    panel_number: int = Field(ge=1)
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: List[str] = Field(default_factory=list)

class ComicStory(BaseModel):
    panels: List[StoryPanel]
