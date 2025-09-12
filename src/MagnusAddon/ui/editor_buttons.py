from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from ankiutils import app
from aqt import gui_hooks
from note.vocabulary.vocabnote import VocabNote
from sysutils.typed import non_optional
from wanikani.wani_downloader import WaniDownloader

if TYPE_CHECKING:
    from anki.notes import Note
    from aqt.editor import Editor


def setup_editor_buttons(buttons: list[str], the_editor: Editor) -> None:
    def ui_action_button(button_text: str, action: Callable[[Note], None]) -> None:
        def inner_action(editor: Editor) -> None:
            action(non_optional(editor.note))
            app.get_ui_utils().refresh()

        buttons.append(the_editor.addButton("", button_text, inner_action))

    ui_action_button("Fetch audio from wanikani", lambda note: WaniDownloader.fetch_audio_from_wanikani(VocabNote(note)))

def init() -> None:
    gui_hooks.editor_did_init_buttons.append(setup_editor_buttons)  # pyright: ignore[reportUnknownMemberType]
