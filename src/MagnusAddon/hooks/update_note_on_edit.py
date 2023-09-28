from anki.notes import Note
from aqt import gui_hooks

from note.mynote import MyNote


def init() -> None:
    def handle_update(note: Note):
        # noinspection PyProtectedMember
        MyNote._on_note_edited(note)

    gui_hooks.editor_did_fire_typing_timer.append(handle_update)