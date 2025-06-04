from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from anki.notes import Note
from ankiutils import app
from autoslot import Slots
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from note.jpnote import JPNote
from note.note_constants import ImmersionKitSentenceNoteFields, NoteFields, NoteTypes, SentenceNoteFields, Tags
from note.notefields.audio_field import WritableAudioField
from note.notefields.json_object_field import JsonObjectField
from note.notefields.sentence_question_field import SentenceQuestionField
from note.notefields.string_field import StringField
from note.notefields.strip_html_on_read_fallback_string_field import StripHtmlOnReadFallbackStringField
from note.notefields.strip_html_on_read_string_field import StripHtmlOnReadStringField
from note.sentences.caching_sentence_configuration_field import CachingSentenceConfigurationField
from note.sentences.parsing_result import ParsingResult
from note.sentences.serialization.parsing_result_serializer import ParsingResultSerializer
from note.sentences.user_fields import SentenceUserFields
from sysutils import ex_sequence, ex_str, kana_utils
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote

class SentenceNote(JPNote, Slots):
    def __init__(self, note: Note) -> None:
        super().__init__(note)
        self.weakref = cast(WeakRef[SentenceNote], self.weakref)

        self._source_answer = StringField(self.weakref, SentenceNoteFields.source_answer)
        self._source_question = StripHtmlOnReadStringField(self.weakref, SentenceNoteFields.source_question)
        self.source_comments: StripHtmlOnReadStringField = StripHtmlOnReadStringField(self.weakref, SentenceNoteFields.source_comments)

        self.user: SentenceUserFields = SentenceUserFields(self.weakref)

        self.question: SentenceQuestionField = SentenceQuestionField(self.weakref, SentenceNoteFields.user_question, SentenceNoteFields.source_question)
        self.answer: StripHtmlOnReadFallbackStringField = StripHtmlOnReadFallbackStringField(self.weakref, SentenceNoteFields.user_answer, SentenceNoteFields.source_answer)
        self._screenshot: StringField = StringField(self.weakref, SentenceNoteFields.screenshot)
        self.audio: WritableAudioField = WritableAudioField(self.weakref, SentenceNoteFields.audio)
        self.configuration: CachingSentenceConfigurationField = CachingSentenceConfigurationField(self.weakref)
        self.parsing_result: JsonObjectField[ParsingResult] = JsonObjectField[ParsingResult](self.weakref, SentenceNoteFields.parsing_result, ParsingResultSerializer())

    def get_question(self) -> str: return self.question.get()
    def get_answer(self) -> str: return self.answer.get()

    def is_studying_read(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Reading)
    def is_studying_listening(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Listening)

    def get_valid_parsed_non_child_words_strings(self) -> list[str]:
        return [w.form for w in self.get_valid_parsed_non_child_words()]

    def get_valid_parsed_non_child_words(self) -> list[CandidateWordVariant]:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        analysis = TextAnalysis(self.get_question(), self.configuration.configuration)
        return analysis.display_word_variants

    def get_direct_dependencies(self) -> set[JPNote]:
        highlighted = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.configuration.highlighted_words()]))
        valid_parsed_roots = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.get_valid_parsed_non_child_words_strings()]))
        kanji = set(self.collection.kanji.with_any_kanji_in(self.extract_kanji()))
        return highlighted | valid_parsed_roots | kanji

    def parse_words_from_expression(self) -> list[str]:
        return TextAnalysis.from_text(self.get_question()).all_words_strings()

    def get_words(self) -> set[str]: return (set(self.parsing_result.get().parsed_words_strings()) | set(self.configuration.highlighted_words())) - self.configuration.incorrect_matches.words()

    def get_parsed_words_notes(self) -> list[VocabNote]:
        return ex_sequence.flatten([app.col().vocab.with_question(q) for q in self.get_valid_parsed_non_child_words_strings()])

    def update_generated_data(self) -> None:
        super().update_generated_data()
        self.update_parsed_words()
        self.set_field(SentenceNoteFields.active_answer, self.get_answer())
        self.set_field(SentenceNoteFields.active_question, self.get_question())

    def update_parsed_words(self, force: bool = False) -> None:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        parsing_result = self.parsing_result.get()
        if not force and parsing_result and parsing_result.sentence == self.get_question() and parsing_result.parser_version == TextAnalysis.version:
            return

        analysis = TextAnalysis(self.get_question(), self.configuration.configuration)
        self.parsing_result.set(ParsingResult.from_analysis(analysis))

    def extract_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    @classmethod
    def create_test_note(cls, question: str, answer: str) -> SentenceNote:
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._source_question.set(question)
        note.user.answer.set(answer)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note

    @classmethod
    def add_sentence(cls, question: str, answer: str, audio: str = "", screenshot: str = "", highlighted_vocab: Optional[set[str]] = None, tags: Optional[set[str]] = None) -> SentenceNote:
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._source_question.set(question)
        note._source_answer.set(answer)
        note._screenshot.set(screenshot)
        note.update_generated_data()

        if not audio.strip():
            note.set_tag(Tags.TTSAudio)
        else:
            audio1 = audio.strip()
            note.audio.set_raw_value(audio1)

        if highlighted_vocab:
            for vocab in highlighted_vocab:
                note.configuration.add_highlighted_word(vocab)

        if tags:
            for tag in tags:
                note.set_tag(tag)

        app.anki_collection().addNote(inner_note)
        return note

    @classmethod
    def import_immersion_kit_sentence(cls, immersion_kit_note: Note) -> SentenceNote:
        created = cls.add_sentence(question=immersion_kit_note[ImmersionKitSentenceNoteFields.question],
                                   answer=immersion_kit_note[ImmersionKitSentenceNoteFields.answer],
                                   audio=immersion_kit_note[ImmersionKitSentenceNoteFields.audio],
                                   screenshot=immersion_kit_note[ImmersionKitSentenceNoteFields.screenshot],
                                   tags={Tags.immersion_kit})

        created.set_field(SentenceNoteFields.id, immersion_kit_note[ImmersionKitSentenceNoteFields.id])
        created.set_field(SentenceNoteFields.reading, immersion_kit_note[ImmersionKitSentenceNoteFields.reading])

        return created

    @classmethod
    def create(cls, question: str) -> SentenceNote:
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._source_question.set(question)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note
