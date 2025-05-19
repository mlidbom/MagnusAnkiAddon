from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils.app import col
from autoslot import Slots
from note.note_constants import NoteFields
from note.notefields.auto_save_wrappers.field_wrapper import FieldWrapper
from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from note.notefields.json_object_field import JsonObjectField
from note.vocabulary.related_vocab.Antonyms import Antonyms
from note.vocabulary.related_vocab.ergative_twin import ErgativeTwin
from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
from note.vocabulary.related_vocab.Synonyms import Synonyms
from sysutils import ex_sequence

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class RelatedVocab(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab = vocab

        self._data: JsonObjectField[RelatedVocabData] = JsonObjectField(vocab, NoteFields.Vocab.related_vocab, RelatedVocabData.serializer)

        self.ergative_twin: ErgativeTwin = ErgativeTwin(vocab, self._data)
        self.synonyms: Synonyms = Synonyms(vocab, self._data)
        self.antonyms: Antonyms = Antonyms(vocab, self._data)
        self.derived_from: FieldWrapper[str] = FieldWrapper(self._data, self._data.get().derived_from)

        self.confused_with: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().confused_with)

    def in_compounds(self) -> list[VocabNote]:
        return col().vocab.with_compound_part(self._vocab().get_question_without_noise_characters())

    def get_direct_dependencies(self) -> set[JPNote]:
        return (set(col().kanji.with_any_kanji_in(list(self._vocab().kanji.extract_main_form_kanji()))) |
                set(ex_sequence.flatten([col().vocab.with_question(compound_part) for compound_part in self._vocab().compound_parts.get()])))
