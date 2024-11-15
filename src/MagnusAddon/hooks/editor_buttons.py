from typing import Callable

from anki.notes import Note
from aqt import gui_hooks
from aqt.editor import Editor

from ankiutils import app
from note import queue_manager
from note.vocabnote import VocabNote
from sysutils.typed import non_optional
from wanikani import wani_note_updater
from wanikani.wani_downloader import WaniDownloader

def setup_editor_buttons(buttons: list[str], the_editor: Editor) -> None:
    def ui_action_button(button_text: str, action: Callable[[Note], None]) -> None:
        def inner_action(editor: Editor) -> None:
            action(non_optional(editor.note))
            app.ui_utils().refresh()

        buttons.append(the_editor.addButton("", button_text, inner_action))

    ui_action_button("Unsuspend with dependencies", queue_manager.unsuspend_with_dependencies)
    ui_action_button("prioritize with dependencies",queue_manager.prioritize_with_dependencies)
    ui_action_button("answer again with zero interval with dependencies", queue_manager.answer_again_with_zero_interval_for_new_note_cards_with_dependencies)
    ui_action_button("Update from wanikani", wani_note_updater.update_from_wanikani)
    ui_action_button("Fetch audio from wanikani", lambda note: WaniDownloader.fetch_audio_from_wanikani(VocabNote(note)))

def init() -> None:
    gui_hooks.editor_did_init_buttons.append(setup_editor_buttons)
