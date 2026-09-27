from datetime import datetime, timezone
from pathlib import Path
from fpdf import FPDF
from PIL import Image
from ..config import get_settings


def _find_font() -> str | None:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    return next((p for p in candidates if Path(p).exists()), None)


def _safe_text(text: str) -> str:
    return text.replace("\u2014", "-").replace("\u2013", "-").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')


def save_pdf(layout: list[dict], title: str = "ComicCraft Comic") -> str:
    settings = get_settings()
    filename = f"comiccraft_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}.pdf"
    output = settings.exports_dir / filename
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    font_path = _find_font()
    if font_path:
        pdf.add_font("ComicFont", "", font_path)
        font = "ComicFont"
    else:
        font = "Helvetica"

    for panel in layout:
        pdf.add_page()
        pdf.set_font(font, size=18)
        pdf.cell(0, 12, _safe_text(f"Panel {panel['panel_number']}: {panel['title']}"), new_x="LMARGIN", new_y="NEXT")
        image_url = panel["image_path"]
        image_path = settings.static_dir / image_url.removeprefix("/static/")
        if image_path.exists():
            with Image.open(image_path) as im:
                w, h = im.size
            max_w, max_h = 180, 115
            scale = min(max_w / w, max_h / h)
            pdf.image(str(image_path), w=w * scale, h=h * scale)
        pdf.ln(5)
        pdf.set_font(font, size=11)
        pdf.multi_cell(0, 6, _safe_text(panel["scene_description"]))
        pdf.ln(2)
        pdf.set_font(font, size=12)
        pdf.multi_cell(0, 7, _safe_text(f"Caption: {panel['caption']}"))
        pdf.multi_cell(0, 7, _safe_text(f"Narration: {panel['narration']}"))
        for line in panel.get("dialogue", []):
            pdf.multi_cell(0, 7, _safe_text(f'“{line}”'))

    pdf.output(str(output))
    return f"/static/exports/{filename}"
