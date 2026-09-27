from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

    gemini_api_key: str = ""
    hf_token: str = ""
    gemini_outline_model: str = "gemini-3.8-flash"
    gemini_story_model: str = "gemini-3.8-flash"
    image_provider: str = "hf"
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    hf_provider: str = "auto"
    local_image_model: str = "runwayml/stable-diffusion-v1-5"
    local_image_steps: int = 20
    local_image_width: int = 768
    local_image_height: int = 768
    panels_count: int = 5
    max_prompt_length: int = 2000
    app_env: str = "development"

    @property
    def templates_dir(self) -> Path:
        return BASE_DIR / "app" / "templates"

    @property
    def static_dir(self) -> Path:
        return BASE_DIR / "static"

    @property
    def panels_dir(self) -> Path:
        return self.static_dir / "panels"

    @property
    def exports_dir(self) -> Path:
        return self.static_dir / "exports"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.panels_dir.mkdir(parents=True, exist_ok=True)
    settings.exports_dir.mkdir(parents=True, exist_ok=True)
    return settings
