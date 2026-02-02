from __future__ import annotations

import gc
from typing import TYPE_CHECKING

from jaslib.task_runners.task_progress_runner import TaskRunner
from jastudio.ankiutils import app, query_builder

if TYPE_CHECKING:
    from anki.notes import NoteId

def convert_immersion_kit_sentences() -> None:
    def convert_note(note_id: NoteId) -> None:
        immersion_kit_note = app.anki_collection().get_note(note_id)
        import jastudio.note.sentences.ankisentencenote

        jastudio.note.sentences.ankisentencenote.AnkiSentenceNote.import_immersion_kit_sentence(immersion_kit_note)
        app.anki_collection().remove_notes([note_id])

    with TaskRunner.current("Converting immersion kit sentences", inhibit_gc=True) as runner:
        immersion_kit_sences = list(app.anki_collection().find_notes(query_builder.immersion_kit_sentences()))
        runner.process_with_progress(immersion_kit_sences, convert_note, "Converting immersion kit sentences", run_gc=True, minimum_items_to_gc=100)

def print_gc_status_and_collect() -> None:
    from jastudio.sysutils import object_instance_tracker
    object_instance_tracker.print_instance_counts()

    app.get_ui_utils().tool_tip(f"Gc.isenabled(): {gc.isenabled()}, Collecting ...", 10000)

    instances = gc.collect()
    app.get_ui_utils().tool_tip(f"collected: {instances} instances", 10000)
    object_instance_tracker.print_instance_counts()
