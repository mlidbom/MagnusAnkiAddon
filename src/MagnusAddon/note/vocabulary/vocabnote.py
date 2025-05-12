from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa
from language_services.jamdict_ex.priority_spec import PrioritySpec
from note.note_constants import Mine, NoteFields
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField
from note.notefields.string_field import StringField
from note.vocabnote_cloner import VocabCloner
from note.vocabulary import vocabnote_generated_data, vocabnote_meta_tag, vocabnote_wanikani_extensions
from note.vocabulary.vocabnote_audio import VocabNoteAudio
from note.vocabulary.vocabnote_conjugator import VocabNoteConjugator
from note.vocabulary.vocabnote_context_sentences import VocabContextSentences
from note.vocabulary.vocabnote_factory import VocabNoteFactory
from note.vocabulary.vocabnote_forms import VocabNoteForms
from note.vocabulary.vocabnote_parts_of_speech import VocabNotePartsOfSpeech
from note.vocabulary.vocabnote_related_notes import VocabNoteRelatedNotes
from note.vocabulary.vocabnote_sentences import VocabNoteSentences
from note.vocabulary.vocabnote_usercompoundparts import VocabNoteUserCompoundParts
from note.vocabulary.vocabnote_wanikani_extensions import VocabNoteWaniExtensions
from note.waninote import WaniNote
from sysutils import ex_sequence, ex_str, kana_utils

if TYPE_CHECKING:
    from anki.notes import Note
    from note.jpnote import JPNote
    from wanikani_api import models

class VocabNote(WaniNote):
    factory: VocabNoteFactory = VocabNoteFactory()
    def __init__(self, note: Note) -> None:
        super().__init__(note)
        self.cloner: VocabCloner = VocabCloner(self)
        self.user_mnemonic: StringField = StringField(self, NoteFields.Vocab.Mnemonic__)
        self.related_notes: VocabNoteRelatedNotes = VocabNoteRelatedNotes(self)
        self.context_sentences: VocabContextSentences = VocabContextSentences(self)
        self.audio: VocabNoteAudio = VocabNoteAudio(self)
        self.sentences: VocabNoteSentences = VocabNoteSentences(self)
        self.forms: VocabNoteForms = VocabNoteForms(self)
        self.parts_of_speech: VocabNotePartsOfSpeech = VocabNotePartsOfSpeech(self)
        self.compound_parts: VocabNoteUserCompoundParts = VocabNoteUserCompoundParts(self)
        self.readings: CommaSeparatedStringsListField = CommaSeparatedStringsListField(self, NoteFields.Vocab.Reading)
        self.conjugator: VocabNoteConjugator = VocabNoteConjugator(self)
        self.user_answer: StringField = StringField(self, NoteFields.Vocab.user_answer)
        self.wani_extensions: VocabNoteWaniExtensions = VocabNoteWaniExtensions(self)


    def __repr__(self) -> str: return f"""{self.get_question()}"""

    def set_kanji(self, value: str) -> None: self.set_field(NoteFields.Vocab.Kanji, value)

    def in_compounds(self) -> list[VocabNote]:
        return self.collection.vocab.with_compound_part(self.get_question_without_noise_characters())

    def get_direct_dependencies(self) -> set[JPNote]:
        return (set(self.collection.kanji.with_any_kanji_in(list(self.extract_main_form_kanji()))) |
                set(ex_sequence.flatten([self.collection.vocab.with_question(compound_part) for compound_part in self.compound_parts.get()])))

    def update_generated_data(self) -> None:
        self.set_field(NoteFields.Vocab.sentence_count, str(len(self.sentences.all())))
        self.set_field(NoteFields.Vocab.active_answer, self.get_answer())

        super().update_generated_data()
        vocabnote_generated_data.update_generated_data(self)

    def extract_main_form_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    def extract_all_kanji(self) -> set[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question() + self.forms.all_raw_string())
        return set(char for char in clean if kana_utils.character_is_kanji(char))

    def is_uk(self) -> bool: return self.has_tag(Mine.Tags.UsuallyKanaOnly)

    def set_reading_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_reading_mnemonic, value)

    def set_component_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Vocab.component_subject_ids, value)

    def priority_spec(self) -> PrioritySpec:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        return lookup.priority_spec() if lookup else PrioritySpec(set())

    def get_meta_tags_html(self: VocabNote, display_extended_sentence_statistics: bool = True) -> str:
        return vocabnote_meta_tag.get_meta_tags_html(self, display_extended_sentence_statistics)

    def generate_and_set_answer(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        dict_lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if dict_lookup.found_words():
            generated = dict_lookup.entries[0].generate_answer()
            self.user_answer.set(generated)

    def requires_exact_match(self) -> bool:
        return self.has_tag(Mine.Tags.requires_exact_match)

    def is_question_overrides_form(self) -> bool: return self.has_tag(Mine.Tags.question_overrides_form)

    @staticmethod
    def _strip_noise_characters(string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")

    def get_question_without_noise_characters(self) -> str: return self._strip_noise_characters(self.get_question())
    def set_question(self, value: str) -> None: self.set_field(NoteFields.Vocab.question, value)

    def get_answer(self) -> str:
        return self.user_answer.get() or self.get_field(NoteFields.Vocab.source_answer)

    def _set_source_answer(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_answer, value)

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        super().update_from_wani(wani_vocab)
        vocabnote_wanikani_extensions.update_from_wani(self, wani_vocab)
