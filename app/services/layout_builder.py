from ..schemas import ComicOutline, ComicStory


def build_comic_layout(outline: ComicOutline, story: ComicStory, image_paths: list[str]) -> list[dict]:
    story_by_number = {p.panel_number: p for p in story.panels}
    layout = []
    for idx, outline_panel in enumerate(outline.panels):
        panel = story_by_number.get(outline_panel.panel_number)
        if panel is None:
            raise RuntimeError(f"Missing story for panel {outline_panel.panel_number}")
        layout.append({
            "panel_number": panel.panel_number,
            "title": panel.title,
            "scene_description": panel.scene_description,
            "caption": panel.caption,
            "narration": panel.narration,
            "dialogue": panel.dialogue,
            "image_prompt": outline_panel.image_prompt,
            "image_path": image_paths[idx],
        })
    return layout
