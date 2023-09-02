from anki.notes import Note
from aqt import gui_hooks

from note.mynote import MyNote
from sysutils.ui_utils import UIUtils


def init() -> None:
    def handle_update(note: Note):
        # noinspection PyProtectedMember
        MyNote._on_note_edited(note)
        #UIUtils.refresh() #todo: this is a rather ugly hack. Surely anki should handle this itself if everything is working right?

    gui_hooks.editor_did_fire_typing_timer.append(handle_update)