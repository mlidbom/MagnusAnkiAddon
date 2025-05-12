from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from anki.notes import Note
from note.jpnote import JPNote
from note.note_constants import ImmersionKitSentenceNoteFields, Mine, NoteFields, NoteTypes, SentenceNoteFields
from note.notefields.audio_field import AudioField
from note.notefields.string_field import StringField
from note.notefields.strip_html_on_read_fallback_string_field import StripHtmlOnReadFallbackStringField
from note.notefields.strip_html_on_read_string_field import StripHtmlOnReadStringField
from note.sentencenote_configuration import CachingSentenceConfigurationField, ParsingResult
from sysutils import ex_sequence, ex_str, kana_utils

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
    from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
    from note.vocabulary.vocabnote import VocabNote

class SentenceNote(JPNote):
    def __init__(self, note: Note) -> None:
        super().__init__(note)
        self._source_answer = StringField(self, SentenceNoteFields.source_answer)
        self._user_question = StringField(self, SentenceNoteFields.user_question)
        self._source_question = StripHtmlOnReadStringField(self, SentenceNoteFields.source_question)
        self.question = StripHtmlOnReadFallbackStringField(self, SentenceNoteFields.user_question, SentenceNoteFields.source_question)
        self.answer = StripHtmlOnReadFallbackStringField(self, SentenceNoteFields.user_answer, SentenceNoteFields.source_answer)
        self._screenshot = StringField(self, SentenceNoteFields.screenshot)
        self.audio = AudioField(self, SentenceNoteFields.audio)
        self._user_answer = StringField(self, SentenceNoteFields.user_answer)
        self.configuration: CachingSentenceConfigurationField = CachingSentenceConfigurationField(self)

    def parsing_result(self) -> ParsingResult: return self.configuration.parsing_result()

    def get_question(self) -> str: return self.question.get()
    def get_answer(self) -> str: return self.answer.get()

    def is_studying_read(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Reading)
    def is_studying_listening(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Listening)

    def get_valid_parsed_non_child_words_strings(self) -> list[str]:
        return [w.form for w in self.get_valid_parsed_non_child_words()]

    def get_valid_parsed_non_child_words(self) -> list[CandidateForm]:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        analysis = TextAnalysis(self.get_question(), self.configuration.incorrect_matches())
        return analysis.display_words

    def get_direct_dependencies(self) -> set[JPNote]:
        highlighted = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.configuration.highlighted_words()]))
        valid_parsed_roots = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.get_valid_parsed_non_child_words_strings()]))
        kanji = set(self.collection.kanji.with_any_kanji_in(self.extract_kanji()))
        return highlighted | valid_parsed_roots | kanji

    def parse_words_from_expression(self) -> list[ExtractedWord]:
        from language_services.janome_ex.word_extraction.word_extractor import jn_extractor
        return jn_extractor.extract_words(self.get_question())

    def get_words(self) -> set[str]: return (set(self.parsing_result().parsed_words_strings()) | set(self.configuration.highlighted_words())) - self.configuration.incorrect_matches_words()

    def get_parsed_words_notes(self) -> list[VocabNote]:
        from ankiutils import app
        return ex_sequence.flatten([app.col().vocab.with_question(q) for q in self.get_valid_parsed_non_child_words_strings()])

    def update_generated_data(self) -> None:
        super().update_generated_data()
        self.update_parsed_words()
        self.set_field(SentenceNoteFields.active_answer, self.get_answer())
        self.set_field(SentenceNoteFields.active_question, self.get_question())

    def update_parsed_words(self, force: bool = False) -> None:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        parsing_result = self.parsing_result()
        if not force and parsing_result and parsing_result.sentence == self.get_question() and parsing_result.parser_version == TextAnalysis.version:
            return

        analysis = TextAnalysis(self.get_question(), self.configuration.incorrect_matches())
        self.configuration.set_parsing_result(analysis)

    def extract_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    @classmethod
    def create_test_note(cls, question: str, answer: str) -> SentenceNote:
        from ankiutils import app
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._source_question.set(question)
        note._user_answer.set(answer)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note

    @classmethod
    def add_sentence(cls, question: str, answer: str, audio: str = "", screenshot: str = "", highlighted_vocab: Optional[set[str]] = None, tags: Optional[set[str]] = None) -> SentenceNote:
        from ankiutils import app
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._source_question.set(question)
        note._source_answer.set(answer)
        note._screenshot.set(screenshot)
        note.update_generated_data()

        if not audio.strip():
            note.set_tag(Mine.Tags.TTSAudio)
        else:
            audio1 = audio.strip()
            note.audio.set(audio1)

        if highlighted_vocab:
            for vocab in highlighted_vocab:
                note.configuration.position_highlighted_word(vocab)

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
                                   tags={Mine.Tags.immersion_kit})

        created.set_field(SentenceNoteFields.id, immersion_kit_note[ImmersionKitSentenceNoteFields.id])
        created.set_field(SentenceNoteFields.reading, immersion_kit_note[ImmersionKitSentenceNoteFields.reading])

        return created

    @classmethod
    def create(cls, question: str) -> SentenceNote:
        from ankiutils import app
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._source_question.set(question)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note
