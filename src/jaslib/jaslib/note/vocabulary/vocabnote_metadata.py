from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.note_constants import NoteFields
from jaslib.note.notefields.integer_field import IntegerField
from jaslib.note.vocabulary import vocabnote_meta_tag

if TYPE_CHECKING:
    from jaslib.note.vocabulary.vocabnote import VocabNote
    from jaslib.sysutils.weak_ref import WeakRef


class VocabNoteMetaData(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab: WeakRef[VocabNote] = vocab

    @property
    def sentence_count(self) -> IntegerField: return IntegerField(self.__vocab, NoteFields.Vocab.sentence_count)

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def meta_tags_html(self, display_extended_sentence_statistics: bool = True, no_sentense_statistics: bool = False) -> str:
        return vocabnote_meta_tag.get_meta_tags_html(self._vocab, display_extended_sentence_statistics, no_sentense_statistics)
