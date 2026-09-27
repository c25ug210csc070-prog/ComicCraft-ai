import re
from pathlib import Path
from uuid import uuid4
from PIL import Image
from ..config import get_settings


def _filename(panel_number: int) -> str:
    return f"panel_{panel_number}_{uuid4().hex[:10]}.png"


def _generate_hf(prompt: str, output_path: Path) -> None:
    from huggingface_hub import InferenceClient
    settings = get_settings()
    if not settings.hf_token:
        raise RuntimeError("HF_TOKEN is required when IMAGE_PROVIDER=hf")
    client = InferenceClient(provider=settings.hf_provider, api_key=settings.hf_token)
    image = client.text_to_image(prompt=prompt, model=settings.hf_image_model)
    image.save(output_path)


def _generate_local(prompt: str, output_path: Path) -> None:
    # Lazy import keeps the normal API installation lightweight.
    import torch
    from diffusers import StableDiffusionPipeline
    settings = get_settings()
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    pipe = StableDiffusionPipeline.from_pretrained(settings.local_image_model, torch_dtype=dtype)
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    image = pipe(
        prompt,
        num_inference_steps=settings.local_image_steps,
        width=settings.local_image_width,
        height=settings.local_image_height,
    ).images[0]
    image.save(output_path)
    del pipe
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def generate_image(prompt: str, panel_number: int) -> str:
    settings = get_settings()
    output_path = settings.panels_dir / _filename(panel_number)
    enhanced = (
        f"{prompt}. Comic panel illustration, strong readable composition, expressive characters, "
        "consistent character appearance, cinematic lighting, no text, no watermark, no logo."
    )
    if settings.image_provider.lower() == "local":
        _generate_local(enhanced, output_path)
    else:
        _generate_hf(enhanced, output_path)
    return f"/static/panels/{output_path.name}"
