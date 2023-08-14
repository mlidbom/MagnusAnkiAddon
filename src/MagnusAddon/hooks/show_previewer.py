from aqt import gui_hooks
from aqt.editor import Editor, EditorMode

from sysutils.utils import UIUtils


def init() -> None:
    gui_hooks.editor_did_load_note.append(register_show_previewer)


def register_show_previewer(editor: Editor):
    if editor.editorMode == EditorMode.EDIT_CURRENT:
        UIUtils.show_current_review_in_preview()
        editor.parentWindow.activateWindow()
