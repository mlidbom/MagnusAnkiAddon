from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from autoslot import Slots
from jaslib.note.jpnote import JPNote
from jaslib.note.note_constants import NoteFields
from jaslib.note.notefields.comma_separated_strings_list_field import MutableCommaSeparatedStringsListField
from jaslib.note.notefields.mutable_string_field import MutableStringField
from jaslib.note.vocabulary import vocabnote_generated_data
from jaslib.note.vocabulary.related_vocab.related_vocab import RelatedVocab
from jaslib.note.vocabulary.vocabnote_audio import VocabNoteAudio
from jaslib.note.vocabulary.vocabnote_cloner import VocabCloner
from jaslib.note.vocabulary.vocabnote_conjugator import VocabNoteConjugator
from jaslib.note.vocabulary.vocabnote_factory import VocabNoteFactory
from jaslib.note.vocabulary.vocabnote_forms import VocabNoteForms
from jaslib.note.vocabulary.vocabnote_kanji import VocabNoteKanji
from jaslib.note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration
from jaslib.note.vocabulary.vocabnote_metadata import VocabNoteMetaData
from jaslib.note.vocabulary.vocabnote_parts_of_speech import VocabNotePartsOfSpeech
from jaslib.note.vocabulary.vocabnote_question import VocabNoteQuestion
from jaslib.note.vocabulary.vocabnote_register import VocabNoteRegister
from jaslib.note.vocabulary.vocabnote_sentences import VocabNoteSentences
from jaslib.note.vocabulary.vocabnote_usercompoundparts import VocabNoteUserCompoundParts
from jaslib.note.vocabulary.vocabnote_userfields import VocabNoteUserfields
from jaslib.sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from jaslib.note.jpnote_data import JPNoteData
    from typed_linq_collections.collections.q_set import QSet

# noinspection PyUnusedFunction
class VocabNote(JPNote, Slots):
    factory: VocabNoteFactory = VocabNoteFactory()
    def __init__(self, data: JPNoteData | None = None) -> None:
        super().__init__(data)
        self.weakref_vocab: WeakRef[VocabNote] = cast(WeakRef[VocabNote], self.weakref)
        self.question: VocabNoteQuestion = VocabNoteQuestion(self.weakref_vocab)

        self.readings: MutableCommaSeparatedStringsListField = MutableCommaSeparatedStringsListField(self.weakref, NoteFields.Vocab.Reading)

        self.user: VocabNoteUserfields = VocabNoteUserfields(self.weakref_vocab)

        self.related_notes: RelatedVocab = RelatedVocab(self.weakref_vocab)
        self.sentences: VocabNoteSentences = VocabNoteSentences(self.weakref_vocab)
        self.forms: VocabNoteForms = VocabNoteForms(self.weakref_vocab)
        self.parts_of_speech: VocabNotePartsOfSpeech = VocabNotePartsOfSpeech(self.weakref_vocab)
        self.compound_parts: VocabNoteUserCompoundParts = VocabNoteUserCompoundParts(self.weakref_vocab)
        self.matching_configuration: VocabNoteMatchingConfiguration = VocabNoteMatchingConfiguration(self.weakref_vocab)

    @override
    def _update_in_cache(self) -> None: self.collection.vocab._cache.refresh_in_cache(self)  # pyright: ignore [reportPrivateUsage]

    @override
    def get_question(self) -> str: return self.question.raw

    @property
    def meta_data(self) -> VocabNoteMetaData: return VocabNoteMetaData(self.weakref_vocab)
    @property
    def kanji(self) -> VocabNoteKanji: return VocabNoteKanji(self.weakref_vocab)
    @property
    def audio(self) -> VocabNoteAudio: return VocabNoteAudio(self.weakref_vocab)
    @property
    def cloner(self) -> VocabCloner: return VocabCloner(self.weakref_vocab)
    @property
    def conjugator(self) -> VocabNoteConjugator: return VocabNoteConjugator(self.weakref_vocab)
    @property
    def source_answer(self) -> MutableStringField: return MutableStringField(self.weakref_vocab, NoteFields.Vocab.source_answer)
    @property
    def active_answer(self) -> MutableStringField: return MutableStringField(self.weakref_vocab, NoteFields.Vocab.active_answer)
    @property
    def register(self) -> VocabNoteRegister: return VocabNoteRegister(self.weakref_vocab)

    @override
    def get_direct_dependencies(self) -> QSet[JPNote]:
        return self.related_notes.get_direct_dependencies()

    @override
    def _on_tags_updated(self) -> None:
        self.matching_configuration = VocabNoteMatchingConfiguration(self.weakref_vocab)

    @override
    def update_generated_data(self) -> None:
        super().update_generated_data()
        vocabnote_generated_data.update_generated_data(self)

    def generate_and_set_answer(self) -> None:
        from jaslib.language_services.jamdict_ex.dict_lookup import DictLookup
        dict_lookup = DictLookup.lookup_vocab_word_or_name(self)
        if dict_lookup.found_words():
            generated = dict_lookup.format_answer()
            self.source_answer.set(generated)

        self.update_generated_data()

    @override
    def get_answer(self) -> str:
        field = self.user.answer
        string_field = self.source_answer
        return field.value or string_field.value
