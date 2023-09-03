from anki.sound import AVTag
from aqt import gui_hooks
from aqt.browser.previewer import BrowserPreviewer
from hooks.timing_hacks import ugly_timing_hacks


def will_play_tags(tags: list[AVTag], _something: str, _view: any):
    if tags:
        if isinstance(_view, BrowserPreviewer):
            if ugly_timing_hacks.typed_in_editor_in_last_seconds(0.1):
                tags.clear()
            if ugly_timing_hacks.reviewer_just_showed_answer():
                tags.clear()

def init() -> None:
    gui_hooks.av_player_will_play_tags.append(will_play_tags)
