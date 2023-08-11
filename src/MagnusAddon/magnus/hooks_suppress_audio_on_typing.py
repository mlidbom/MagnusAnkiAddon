from typing import *

from anki.notes import Note
from anki.sound import AVTag
from aqt import gui_hooks
import time

class suppress_audio_data:
    _last_typing_time = 0.0
    _last_typing_note: Note
def typed_in_editor(note:Note):
    suppress_audio_data._last_typing_time = time.time()
    suppress_audio_data._last_typing_note = note

def will_play_tags(tags: list[AVTag], something:str, view:Any):
    if time.time() - suppress_audio_data._last_typing_time < 0.1:
        tags.clear()

gui_hooks.editor_did_fire_typing_timer.append(typed_in_editor)
gui_hooks.av_player_will_play_tags.append(will_play_tags)