from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa  # pyright: ignore[reportUnusedImport]
from ex_autoslot import ProfilableAutoSlots
from note.jpnote import JPNote
from note.note_constants import NoteFields
from note.notefields.comma_separated_strings_list_field import MutableCommaSeparatedStringsListField
from note.notefields.mutable_string_field import MutableStringField
from note.vocabnote_cloner import VocabCloner
from note.vocabulary import vocabnote_generated_data
from note.vocabulary.related_vocab.related_vocab import RelatedVocab
from note.vocabulary.vocabnote_audio import VocabNoteAudio
from note.vocabulary.vocabnote_conjugator import VocabNoteConjugator
from note.vocabulary.vocabnote_factory import VocabNoteFactory
from note.vocabulary.vocabnote_forms import VocabNoteForms
from note.vocabulary.vocabnote_kanji import VocabNoteKanji
from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration
from note.vocabulary.vocabnote_metadata import VocabNoteMetaData
from note.vocabulary.vocabnote_parts_of_speech import VocabNotePartsOfSpeech
from note.vocabulary.vocabnote_question import VocabNoteQuestion
from note.vocabulary.vocabnote_sentences import VocabNoteSentences
from note.vocabulary.vocabnote_usercompoundparts import VocabNoteUserCompoundParts
from note.vocabulary.vocabnote_userfields import VocabNoteUserfields
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from anki.notes import Note


class VocabNote(JPNote, ProfilableAutoSlots):
    factory: VocabNoteFactory = VocabNoteFactory()
    def __init__(self, note: Note) -> None:
        super().__init__(note)
        self.weakref_vocab: WeakRef[VocabNote] = cast(WeakRef[VocabNote], self.weakref)

        self.question: VocabNoteQuestion = VocabNoteQuestion(self.weakref_vocab)

        self.readings: MutableCommaSeparatedStringsListField = MutableCommaSeparatedStringsListField(self.weakref, NoteFields.Vocab.Reading)

        self.user: VocabNoteUserfields = VocabNoteUserfields(self.weakref_vocab)

        self._source_answer: MutableStringField = MutableStringField(self.weakref, NoteFields.Vocab.source_answer)
        self.active_answer: MutableStringField = MutableStringField(self.weakref, NoteFields.Vocab.active_answer)

        self.cloner: VocabCloner = VocabCloner(self.weakref_vocab)
        self.related_notes: RelatedVocab = RelatedVocab(self.weakref_vocab)
        self.audio: VocabNoteAudio = VocabNoteAudio(self.weakref_vocab)
        self.sentences: VocabNoteSentences = VocabNoteSentences(self.weakref_vocab)
        self.forms: VocabNoteForms = VocabNoteForms(self.weakref_vocab)
        self.parts_of_speech: VocabNotePartsOfSpeech = VocabNotePartsOfSpeech(self.weakref_vocab)
        self.compound_parts: VocabNoteUserCompoundParts = VocabNoteUserCompoundParts(self.weakref_vocab)
        self.conjugator: VocabNoteConjugator = VocabNoteConjugator(self.weakref_vocab)
        self.kanji: VocabNoteKanji = VocabNoteKanji(self.weakref_vocab)
        self.meta_data: VocabNoteMetaData = VocabNoteMetaData(self.weakref_vocab)
        self.matching_configuration: VocabNoteMatchingConfiguration = VocabNoteMatchingConfiguration(self.weakref_vocab)

    @override
    def get_direct_dependencies(self) -> set[JPNote]:
        return self.related_notes.get_direct_dependencies()

    @override
    def update_generated_data(self) -> None:
        super().update_generated_data()
        vocabnote_generated_data.update_generated_data(self)

    def generate_and_set_answer(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        dict_lookup = DictLookup.lookup_vocab_word_or_name(self)
        if dict_lookup.found_words():
            generated = dict_lookup.entries[0].generate_answer()
            self.user.answer.set(generated)

        self.update_generated_data()

    @override
    def get_answer(self) -> str:
        field = self.user.answer
        string_field = self._source_answer
        return field.value or string_field.value
