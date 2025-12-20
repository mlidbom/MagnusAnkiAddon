from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.jamdict_ex.priority_spec import PrioritySpec
from note.note_constants import NoteFields
from note.notefields.integer_field import IntegerField
from note.vocabulary import vocabnote_meta_tag

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class VocabNoteMetaData(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab: WeakRef[VocabNote] = vocab
        self.sentence_count: IntegerField = IntegerField(vocab, NoteFields.Vocab.sentence_count)

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def meta_tags_html(self, display_extended_sentence_statistics: bool = True, no_sentense_statistics: bool = False) -> str:
        return vocabnote_meta_tag.get_meta_tags_html(self._vocab, display_extended_sentence_statistics, no_sentense_statistics)

    def priority_spec(self) -> PrioritySpec:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        lookup = DictLookup.lookup_vocab_word_or_name(self._vocab)
        return lookup.priority_spec() if lookup else PrioritySpec(set())
