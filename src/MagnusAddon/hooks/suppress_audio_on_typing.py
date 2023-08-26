from anki.notes import Note
from anki.sound import AVTag
from aqt import gui_hooks
import time

from aqt.browser.previewer import BrowserPreviewer


class SuppressAudioData:
    last_typing_time = 0.0
    reviewer_showed_answer_time = 0.0
    _last_typing_note: Note

def on_reviewer_show_answer(_card: any) -> None:
    SuppressAudioData.reviewer_showed_answer_time = time.time()


def typed_in_editor(note:Note):
    SuppressAudioData.last_typing_time = time.time()
    SuppressAudioData._last_typing_note = note

def will_play_tags(tags: list[AVTag], _something: str, _view: any):
    if tags:
        if isinstance(_view, BrowserPreviewer):
            if time.time() - SuppressAudioData.last_typing_time < 0.1:
                tags.clear()
            if time.time() - SuppressAudioData.reviewer_showed_answer_time < 1:
                tags.clear()

def init() -> None:
    gui_hooks.reviewer_did_show_answer.append(on_reviewer_show_answer)
    gui_hooks.editor_did_fire_typing_timer.append(typed_in_editor)
    gui_hooks.av_player_will_play_tags.append(will_play_tags)
