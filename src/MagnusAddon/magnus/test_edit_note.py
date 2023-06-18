import aqt.editor
from aqt import gui_hooks


from .wanikani_note import *


def edit_note(kanji_note: WaniKanjiNote):
    old_value = kanji_note.get_kanji_meaning()
    new_value = old_value + " edited"
    kanji_note.set_kanji_meaning(new_value)

def setup_buttons(buttons, the_editor: aqt.editor.Editor):
    btn = the_editor.addButton("", "Edit note",
                               lambda local_editor: edit_note(WaniKanjiNote(local_editor.note)))
    buttons.append(btn)


gui_hooks.editor_did_init_buttons.append(setup_buttons)
