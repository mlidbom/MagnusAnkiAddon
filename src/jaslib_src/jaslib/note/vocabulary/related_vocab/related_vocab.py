from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from typed_linq_collections.collections.q_set import QSet
from typed_linq_collections.q_iterable import query

from jaslib import app
from jaslib.note.note_constants import NoteFields
from jaslib.note.notefields.auto_save_wrappers.field_wrapper import FieldWrapper
from jaslib.note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from jaslib.note.notefields.json_object_field import MutableSerializedObjectField
from jaslib.note.vocabulary.related_vocab.Antonyms import Antonyms
from jaslib.note.vocabulary.related_vocab.ergative_twin import ErgativeTwin
from jaslib.note.vocabulary.related_vocab.perfect_synonyms import PerfectSynonyms
from jaslib.note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
from jaslib.note.vocabulary.related_vocab.SeeAlso import SeeAlso
from jaslib.note.vocabulary.related_vocab.Synonyms import Synonyms
from jaslib.sysutils.lazy import Lazy

if TYPE_CHECKING:
    from jaslib.note.jpnote import JPNote
    from jaslib.note.kanjinote import KanjiNote
    from jaslib.note.vocabulary.vocabnote import VocabNote
    from jaslib.sysutils.weak_ref import WeakRef

class RelatedVocab(Slots): # todo performance: memory: do we need to cache all of this, could it be created on demand by properties instead?
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab

        self._data: MutableSerializedObjectField[RelatedVocabData] = MutableSerializedObjectField(vocab, NoteFields.Vocab.related_vocab, RelatedVocabData.serializer())

        self.ergative_twin: ErgativeTwin = ErgativeTwin(vocab, self._data)
        self.synonyms: Synonyms = Synonyms(vocab, self._data)
        self.perfect_synonyms: PerfectSynonyms = PerfectSynonyms(vocab, FieldSetWrapper[str].for_json_object_field(self._data, self._data.get().perfect_synonyms))
        self.antonyms: Antonyms = Antonyms(vocab, self._data)
        self.see_also: SeeAlso = SeeAlso(vocab, self._data)
        self.derived_from: FieldWrapper[str, RelatedVocabData] = FieldWrapper(self._data, self._data.get().derived_from)

        self.confused_with: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().confused_with)  # pyright: ignore[reportUnknownMemberType]

        self._in_compound_ids: Lazy[QSet[int]] = Lazy(lambda: QSet(voc.get_id() for voc in vocab().related_notes.in_compounds()))

    @property
    def in_compound_ids(self) -> QSet[int]: return self._in_compound_ids()

    def in_compounds(self) -> list[VocabNote]:
        return app.col().vocab.with_compound_part(self._vocab().question.disambiguation_name)

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

    def get_direct_dependencies(self) -> QSet[JPNote]:
        return QSet.create(self._main_form_kanji_notes, self._vocab().compound_parts.all_notes())
