from __future__ import annotations

from typing import TYPE_CHECKING

from anki.consts import QUEUE_TYPE_SUSPENDED
from anki.notes import Note, NoteId
from jaslib.task_runners.task_progress_runner import TaskRunner
from jaspythonutils.sysutils import typed
from jaspythonutils.sysutils.memory_usage import string_auto_interner
from jaspythonutils.sysutils.typed import non_optional
from jastudio.anki_extentions.note_ex import NoteEx
from JAStudio.Core import App
from JAStudio.Core.Note import NoteTypes
from JAStudio.Core.Note.Collection import CardStudyingStatus
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.dbproxy import Row
    from jastudio.anki_extentions.card_ex import CardEx

def update_note_in_studying_cache(note: Note) -> None:
    for card_ex in NoteEx(note).cards():
        update_card_in_studying_cache(card_ex)

def update_card_in_studying_cache(card_ex: CardEx) -> None:
    status = CardStudyingStatus(card_ex.note_ex().id, card_ex.card_type, card_ex.is_suspended(), card_ex.note_ex().note_type.name)
    if status.NoteTypeName == NoteTypes.Kanji:
        App.Col().Kanji.Cache.SetStudyingStatuses([status])
    if status.NoteTypeName == NoteTypes.Vocab:
        App.Col().Vocab.Cache.SetStudyingStatuses([status])
    if status.NoteTypeName == NoteTypes.Sentence:
        App.Col().Sentences.Cache.SetStudyingStatuses([status])

class CardStudyingStatusFactory:
    @classmethod
    def from_row(cls, row: Row) -> CardStudyingStatus:
        note_id: NoteId = NoteId(typed.int_(row[0]))  # pyright: ignore[reportAny]
        card_type: str = string_auto_interner.auto_intern(typed.str_(row[1]))  # pyright: ignore[reportAny]
        is_suspended: bool = typed.int_(row[2]) == QUEUE_TYPE_SUSPENDED  # pyright: ignore[reportAny]
        note_type_name: str = string_auto_interner.auto_intern(typed.str_(row[3]))  # pyright: ignore[reportAny]

        return CardStudyingStatus(note_id, card_type, is_suspended, note_type_name)

# don't use temporary variables, it will break our memory profiling using tracemalloc
def fetch_card_studying_statuses(col: Collection, ) -> list[CardStudyingStatus]:
    sql_query = f"""
        SELECT cards.nid as note_id, templates.name as card_type, cards.queue as queue, notetypes.name as note_type
        FROM cards
        JOIN notes ON cards.nid = notes.id
        JOIN notetypes on notetypes.id = notes.mid
        JOIN templates ON templates.ntid = notes.mid and templates.ord = cards.ord
        WHERE notetypes.name COLLATE NOCASE IN ('{NoteTypes.Sentence}', '{NoteTypes.Vocab}', '{NoteTypes.Kanji}')
    """

    with TaskRunner.current("Fetching card studying status from Anki db") as task_runner:
        return task_runner.RunOnBackgroundThreadWithSpinningProgressDialog(
                "Fetching card studying status from Anki db",
                lambda: query(non_optional(col.db).all(sql_query)).select(CardStudyingStatusFactory.from_row).to_list())
