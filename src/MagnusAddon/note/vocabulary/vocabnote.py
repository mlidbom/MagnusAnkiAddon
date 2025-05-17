from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa
from autoslot import Slots
from note.note_constants import Mine, NoteFields
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField
from note.notefields.string_field import StringField
from note.vocabnote_cloner import VocabCloner
from note.vocabulary import vocabnote_generated_data
from note.vocabulary.vocabnote_audio import VocabNoteAudio
from note.vocabulary.vocabnote_conjugator import VocabNoteConjugator
from note.vocabulary.vocabnote_context_sentences import VocabContextSentences
from note.vocabulary.vocabnote_factory import VocabNoteFactory
from note.vocabulary.vocabnote_forms import VocabNoteForms
from note.vocabulary.vocabnote_kanji import VocabNoteKanji
from note.vocabulary.vocabnote_matching_rules import VocabNoteMatching
from note.vocabulary.vocabnote_metadata import VocabNoteMetaData
from note.vocabulary.vocabnote_parts_of_speech import VocabNotePartsOfSpeech
from note.vocabulary.vocabnote_related_notes import VocabNoteRelatedNotes
from note.vocabulary.vocabnote_sentences import VocabNoteSentences
from note.vocabulary.vocabnote_usercompoundparts import VocabNoteUserCompoundParts
from note.vocabulary.vocabnote_userfields import VocabNoteUserfields
from note.vocabulary.vocabnote_wanikani_extensions import VocabNoteWaniExtensions
from note.waninote import WaniNote
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from anki.notes import Note
    from note.jpnote import JPNote
    from wanikani_api import models

class VocabNote(WaniNote, Slots):
    __slots__ = ["__weakref__"]
    factory: VocabNoteFactory = VocabNoteFactory()
    def __init__(self, note: Note) -> None:
        super().__init__(note)
        self.weakref: WeakRef[VocabNote] = WeakRef(self)

        self.readings: CommaSeparatedStringsListField = CommaSeparatedStringsListField(self.weakref, NoteFields.Vocab.Reading)

        self.user: VocabNoteUserfields = VocabNoteUserfields(self.weakref)

        self._source_answer: StringField = StringField(self.weakref, NoteFields.Vocab.source_answer)
        self.active_answer: StringField = StringField(self.weakref, NoteFields.Vocab.active_answer)

        self.cloner: VocabCloner = VocabCloner(self.weakref)
        self.related_notes: VocabNoteRelatedNotes = VocabNoteRelatedNotes(self.weakref)
        self.context_sentences: VocabContextSentences = VocabContextSentences(self.weakref)
        self.audio: VocabNoteAudio = VocabNoteAudio(self.weakref)
        self.sentences: VocabNoteSentences = VocabNoteSentences(self.weakref)
        self.forms: VocabNoteForms = VocabNoteForms(self.weakref)
        self.parts_of_speech: VocabNotePartsOfSpeech = VocabNotePartsOfSpeech(self.weakref)
        self.compound_parts: VocabNoteUserCompoundParts = VocabNoteUserCompoundParts(self.weakref)
        self.conjugator: VocabNoteConjugator = VocabNoteConjugator(self.weakref)
        self.wani_extensions: VocabNoteWaniExtensions = VocabNoteWaniExtensions(self.weakref)
        self.kanji: VocabNoteKanji = VocabNoteKanji(self.weakref)
        self.meta_data: VocabNoteMetaData = VocabNoteMetaData(self.weakref)
        self.matching_rules: VocabNoteMatching = VocabNoteMatching(self.weakref)

    def __repr__(self) -> str: return f"""{self.get_question()}"""

    def get_direct_dependencies(self) -> set[JPNote]:
        return self.related_notes.get_direct_dependencies()

    def update_generated_data(self) -> None:
        self.meta_data.sentence_count.set(len(self.sentences.all()))
        self.active_answer.set(self.get_answer())
        self.matching_rules.save()

        super().update_generated_data()
        vocabnote_generated_data.update_generated_data(self)

    def generate_and_set_answer(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        dict_lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if dict_lookup.found_words():
            generated = dict_lookup.entries[0].generate_answer()
            self.user.answer.set(generated)

    def get_question_without_noise_characters(self) -> str: return self.get_question().replace(Mine.VocabPrefixSuffixMarker, "")
    def set_question(self, value: str) -> None: self.set_field(NoteFields.Vocab.question, value)

    def get_answer(self) -> str:
        return self.user.answer.get() or self._source_answer.get()

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        super().update_from_wani(wani_vocab)
        self.wani_extensions.update_from_wani(wani_vocab)
