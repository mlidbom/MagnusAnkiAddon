from __future__ import annotations

from typing import TYPE_CHECKING

from aqt import gui_hooks
from aqt.import_export.import_dialog import ImportDialog

from jastudio.batches import local_note_updater

if TYPE_CHECKING:
    from anki.collection import OpChanges


def import_immersion_kit_sentences_if_this_operation_came_from_the_import_dialog(_: OpChanges, source: object | None) -> None:
    if isinstance(source, ImportDialog):
        local_note_updater.convert_immersion_kit_sentences()

def init() -> None:
    gui_hooks.operation_did_execute.append(import_immersion_kit_sentences_if_this_operation_came_from_the_import_dialog)  # pyright: ignore [reportUnknownMemberType]
