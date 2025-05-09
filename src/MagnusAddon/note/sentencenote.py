from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.notefields.string_note_field import AudioField, FallbackStringField, ReadOnlyNewlineSeparatedValuesField, StringField, StripHtmlOnReadStringField
from note.sentencenote_configuration import CachingSentenceConfigurationField, ParsingResult

from sysutils.ex_str import newline

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
    from note.vocabnote import VocabNote

from note.jpnote import JPNote
from sysutils import ex_sequence, kana_utils
from sysutils import ex_str
from note.note_constants import ImmersionKitSentenceNoteFields, Mine, NoteFields, SentenceNoteFields, NoteTypes
from anki.notes import Note

class SentenceNote(JPNote):
    def __init__(self, note: Note):
        super().__init__(note)
        self._source_answer = StringField(self, SentenceNoteFields.source_answer)
        self._user_question = StringField(self, SentenceNoteFields.user_question)
        self._source_question = StripHtmlOnReadStringField(self, SentenceNoteFields.source_question)
        self.question = FallbackStringField(self, SentenceNoteFields.user_question, SentenceNoteFields.source_question)
        self.answer = FallbackStringField(self, SentenceNoteFields.user_answer, SentenceNoteFields.source_answer)
        self._screenshot = StringField(self, SentenceNoteFields.screenshot)
        self.audio = AudioField(self, SentenceNoteFields.audio)
        self._user_answer = StringField(self, SentenceNoteFields.user_answer)
        self._user_excluded_vocab = ReadOnlyNewlineSeparatedValuesField(self, SentenceNoteFields.user_excluded_vocab)
        self._configuration = CachingSentenceConfigurationField(self)


    def parsing_result(self) -> ParsingResult: return self._configuration.parsing_result()

    def get_question(self) -> str: return self.question.get()
    def get_answer(self) -> str: return self.answer.get()

    def _set_user_word_exclusions(self, exclusions: set[WordExclusion]) -> None:
        self._configuration.set_incorrect_matches(exclusions)
        self.update_parsed_words(force=True)

    def _set_user_extra_vocab(self, extra: list[str]) -> None: return self.set_field(SentenceNoteFields.user_extra_vocab, newline.join(extra))
    def position_extra_vocab(self, vocab: str, index:int = -1) -> None:
        vocab = vocab.strip()
        self.remove_excluded_vocab(vocab)
        vocab_list = self.get_user_highlighted_vocab()
        if vocab in vocab_list:
            vocab_list.remove(vocab)

        if index == -1:
            vocab_list.append(vocab)
        else:
            vocab_list.insert(index, vocab)

        self._set_user_extra_vocab(vocab_list)

    def remove_extra_vocab(self, vocab: str) -> None:
        self._configuration.remove_higlighted_word(vocab)

    def remove_excluded_vocab(self, vocab: str) -> None:
        exclusion = WordExclusion.from_string(vocab)
        excluded = self._configuration.incorrect_matches()
        new_excluded = {e for e in excluded if not exclusion.covers(e)}
        self._set_user_word_exclusions(new_excluded)

    def exclude_vocab(self, vocab: str) -> None:
        exclusion = WordExclusion.from_string(vocab)
        self.remove_extra_vocab(exclusion.word)
        excluded = set(self._configuration.incorrect_matches())
        excluded.add(exclusion)
        self._set_user_word_exclusions(excluded)

    def is_studying_read(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Reading)
    def is_studying_listening(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Listening)


    def get_valid_parsed_non_child_words_strings(self) -> list[str]:
        return [w.form for w in self.get_valid_parsed_non_child_words()]

    def get_valid_parsed_non_child_words(self) -> list[CandidateForm]:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        analysis = TextAnalysis(self.get_question(), list(self._configuration.incorrect_matches()))
        return analysis.display_words

    def get_direct_dependencies(self) -> set[JPNote]:
        highlighted = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.get_user_highlighted_vocab()]))
        valid_parsed_roots = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.get_valid_parsed_non_child_words_strings()]))
        kanji = set(self.collection.kanji.with_any_kanji_in(self.extract_kanji()))
        return highlighted | valid_parsed_roots | kanji

    def get_user_highlighted_vocab(self) -> list[str]: return ex_str.extract_newline_separated_values(self.get_field(SentenceNoteFields.user_extra_vocab))

    def parse_words_from_expression(self) -> list[ExtractedWord]:
        from language_services.janome_ex.word_extraction.word_extractor import jn_extractor
        return jn_extractor.extract_words(self.get_question())

    def get_parsed_words(self) -> list[str]: return self.parsing_result().parsed_words_strings()

    def get_words(self) -> set[str]: return (set(self.get_parsed_words()) | set(self.get_user_highlighted_vocab())) - self._configuration.incorrect_matches_words()

    def get_parsed_words_notes(self) -> list[VocabNote]:
        from ankiutils import app
        return ex_sequence.flatten([app.col().vocab.with_question(q) for q in self.get_valid_parsed_non_child_words_strings()])


    def update_generated_data(self) -> None:
        super().update_generated_data()
        self.update_parsed_words()
        self.set_field(SentenceNoteFields.active_answer, self.get_answer())
        self.set_field(SentenceNoteFields.active_question, self.get_question())
        self._configuration.incorrect_matches()#just trigger access to update it

    def update_parsed_words(self, force:bool = False) -> None:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        parsing_result = self.parsing_result()
        if not force and parsing_result and parsing_result.sentence == self.get_question() and parsing_result.parser_version == TextAnalysis.version:
            return

        analysis = TextAnalysis(self.get_question(), self._configuration.incorrect_matches())
        self._configuration.set_parsing_result(analysis)


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
    def add_sentence(cls, question: str, answer:str, audio:str = "", screenshot:str = "", highlighted_vocab: Optional[set[str]] = None, tags: Optional[set[str]] = None) -> SentenceNote:
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
                note.position_extra_vocab(vocab)

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
    def create(cls, question:str) -> SentenceNote:
        from ankiutils import app
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._source_question.set(question)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note
