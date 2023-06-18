from typing import List

import aqt
from anki.notes import Note
from aqt import mw, gui_hooks, dialogs
from .wanikani_note import *

from .my_anki import *
from .wani_constants import *


def edit_note(kanji_note: WaniKanjiNote):
    old_value = kanji_note.get_meaning()
    new_value = old_value + " edited"
    kanji_note.set_meaning(new_value)

def setup_buttons(buttons, the_editor: aqt.editor.Editor):
    btn = the_editor.addButton("", "Edit note",
                               lambda local_editor: edit_note(WaniKanjiNote(local_editor.note)))
    buttons.append(btn)


gui_hooks.editor_did_init_buttons.append(setup_buttons)
