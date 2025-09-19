from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from ex_autoslot import AutoSlots
from note.note_constants import NoteFields
from note.notefields.auto_save_wrappers.field_wrapper import FieldWrapper
from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from note.notefields.json_object_field import MutableSerializedObjectField
from note.vocabulary.related_vocab.Antonyms import Antonyms
from note.vocabulary.related_vocab.ergative_twin import ErgativeTwin
from note.vocabulary.related_vocab.perfect_synonyms import PerfectSynonyms
from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
from note.vocabulary.related_vocab.SeeAlso import SeeAlso
from note.vocabulary.related_vocab.Synonyms import Synonyms
from sysutils.collections.queryable.q_iterable import query
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from note.kanjinote import KanjiNote
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.collections.queryable.q_iterable import QSet
    from sysutils.weak_ref import WeakRef

class RelatedVocab(AutoSlots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab

        self._data: MutableSerializedObjectField[RelatedVocabData] = MutableSerializedObjectField(vocab, NoteFields.Vocab.related_vocab, RelatedVocabData.serializer)

        self.ergative_twin: ErgativeTwin = ErgativeTwin(vocab, self._data)
        self.synonyms: Synonyms = Synonyms(vocab, self._data)
        self.perfect_synonyms: PerfectSynonyms = PerfectSynonyms(vocab, FieldSetWrapper[str].for_json_object_field(self._data, self._data.get().perfect_synonyms))
        self.antonyms: Antonyms = Antonyms(vocab, self._data)
        self.see_also: SeeAlso = SeeAlso(vocab, self._data)
        self.derived_from: FieldWrapper[str, RelatedVocabData] = FieldWrapper(self._data, self._data.get().derived_from)

        self.confused_with: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().confused_with)  # pyright: ignore[reportUnknownMemberType]

        self._in_compound_ids: Lazy[set[int]] = Lazy(lambda: {voc.get_id() for voc in vocab().related_notes.in_compounds()})

    @property
    def in_compound_ids(self) -> set[int]: return self._in_compound_ids()

    def in_compounds(self) -> list[VocabNote]:
        return app.col().vocab.with_compound_part(self._vocab().question.without_noise_characters)

    def homophones_notes(self) -> QSet[VocabNote]:
        return (query(self._vocab().readings.get())
                .select_many(app.col().vocab.with_reading)
                .where(lambda homophone: homophone != self._vocab())
                .to_set())

    def stems_notes(self) -> QSet[VocabNote]:
        return (self._vocab().conjugator.get_stems_for_primary_form()
                .select_many(app.col().vocab.with_question)
                .to_set())  # ex_sequence.flatten([app.col().vocab.with_question(stem) for stem in (_vocab_note.conjugator.get_stems_for_primary_form())])

    @property
    def _main_form_kanji_notes(self) -> QSet[KanjiNote]:
        return app.col().kanji.with_any_kanji_in(self._vocab().kanji.extract_main_form_kanji()).to_set()

    def get_direct_dependencies(self) -> set[JPNote]:
        return set(self._main_form_kanji_notes | self._vocab().compound_parts.all_notes())
