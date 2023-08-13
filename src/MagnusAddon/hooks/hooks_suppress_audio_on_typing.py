from anki.notes import Note
from anki.sound import AVTag
from aqt import gui_hooks
import time

class SuppressAudioData:
    last_typing_time = 0.0
    _last_typing_note: Note

def typed_in_editor(note:Note):
    SuppressAudioData.last_typing_time = time.time()
    SuppressAudioData._last_typing_note = note

def will_play_tags(tags: list[AVTag], _something: str, _view: any):
    if time.time() - SuppressAudioData.last_typing_time < 0.05:
        tags.clear()

def setup():
    gui_hooks.editor_did_fire_typing_timer.append(typed_in_editor)
    gui_hooks.av_player_will_play_tags.append(will_play_tags)
