from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from anki.notes import Note
from ankiutils import app
from ex_autoslot import ProfilableAutoSlots
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from note.jpnote import JPNote
from note.note_constants import ImmersionKitSentenceNoteFields, NoteFields, NoteTypes, SentenceNoteFields, Tags
from note.notefields.audio_field import WritableAudioField
from note.notefields.json_object_field import MutableSerializedObjectField
from note.notefields.mutable_string_field import MutableStringField
from note.notefields.sentence_question_field import SentenceQuestionField
from note.notefields.strip_html_on_read_fallback_string_field import StripHtmlOnReadFallbackStringField
from note.sentences.caching_sentence_configuration_field import CachingSentenceConfigurationField
from note.sentences.parsing_result import ParsingResult
from note.sentences.serialization.parsing_result_serializer import ParsingResultSerializer
from note.sentences.user_fields import SentenceUserFields
from sysutils import ex_sequence, ex_str, kana_utils
from sysutils.collections.linq.q_iterable import QList
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote

class SentenceNote(JPNote, ProfilableAutoSlots):
    def __init__(self, note: Note) -> None:
        super().__init__(note)
        self.weakref_sentence: WeakRef[SentenceNote] = cast(WeakRef[SentenceNote], self.weakref)

        self.id: MutableStringField = MutableStringField(self.weakref, SentenceNoteFields.id)
        self.reading: MutableStringField = MutableStringField(self.weakref, SentenceNoteFields.reading)

        self.active_question: MutableStringField = MutableStringField(self.weakref, SentenceNoteFields.active_question)
        self.active_answer: MutableStringField = MutableStringField(self.weakref, SentenceNoteFields.active_answer)

        self._source_answer: MutableStringField = MutableStringField(self.weakref, SentenceNoteFields.source_answer)
        self.source_question: MutableStringField = MutableStringField(self.weakref, SentenceNoteFields.source_question)
        self.source_comments: MutableStringField = MutableStringField(self.weakref, SentenceNoteFields.source_comments)

        self.user: SentenceUserFields = SentenceUserFields(self.weakref_sentence)

        self.question: SentenceQuestionField = SentenceQuestionField(self.user.question, self.source_question)
        self.answer: StripHtmlOnReadFallbackStringField = StripHtmlOnReadFallbackStringField(self.user.answer, self._source_answer)
        self._screenshot: MutableStringField = MutableStringField(self.weakref, SentenceNoteFields.screenshot)
        self.audio: WritableAudioField = WritableAudioField(self.weakref, SentenceNoteFields.audio)
        self.configuration: CachingSentenceConfigurationField = CachingSentenceConfigurationField(self.weakref_sentence)
        self.parsing_result: MutableSerializedObjectField[ParsingResult] = MutableSerializedObjectField[ParsingResult](self.weakref, SentenceNoteFields.parsing_result, ParsingResultSerializer())

    @override
    def get_question(self) -> str: return self.question.get()
    @override
    def get_answer(self) -> str: return self.answer.get()

    def is_studying_read(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Reading)
    def is_studying_listening(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Listening)

    def get_valid_parsed_non_child_words_strings(self) -> QList[str]:
        return self.get_valid_parsed_non_child_words().select(lambda word: word.form).to_list()  #[w.form for w in self.get_valid_parsed_non_child_words()]

    def get_valid_parsed_non_child_words(self) -> QList[CandidateWordVariant]:
        return self.create_analysis().display_word_variants

    def create_analysis(self) -> TextAnalysis:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        return TextAnalysis(self.get_question(), self.configuration.configuration)

    @override
    def get_direct_dependencies(self) -> set[JPNote]:
        highlighted = self.configuration.highlighted_vocab
        displayed_vocab = {voc for voc in {app.col().vocab.with_id_or_none(voc.vocab_id)
                                           for voc in self.parsing_result.get().parsed_words
                                           if voc.is_displayed}
                           if voc is not None}
        kanji = set(self.collection.kanji.with_any_kanji_in(self.extract_kanji()))
        return set(highlighted | displayed_vocab | kanji)

    def parse_words_from_expression(self) -> list[str]:
        return TextAnalysis.from_text(self.get_question()).all_words_strings()

    def get_words(self) -> set[str]: return (set(self.parsing_result.get().parsed_words_strings()) | set(self.configuration.highlighted_words())) - self.configuration.incorrect_matches.words()

    def get_parsed_words_notes(self) -> list[VocabNote]:
        return (self.get_valid_parsed_non_child_words_strings()
                .select_many(app.col().vocab.with_question).to_list()) #ex_sequence.flatten([app.col().vocab.with_question(q) for q in self.get_valid_parsed_non_child_words_strings()])

    @override
    def update_generated_data(self) -> None:
        super().update_generated_data()
        self.update_parsed_words()
        self.active_answer.set(self.get_answer())
        self.active_question.set(self.get_question())

    def update_parsed_words(self, force: bool = False) -> None:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        parsing_result = self.parsing_result.get()
        if not force and parsing_result and parsing_result.sentence == self.get_question() and parsing_result.parser_version == TextAnalysis.version:
            return

        analysis = self.create_analysis()
        self.parsing_result.set(ParsingResult.from_analysis(analysis))

    def extract_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    @classmethod
    def create_test_note(cls, question: str, answer: str) -> SentenceNote:
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note.source_question.set(question)
        note.user.answer.set(answer)
        note.update_generated_data()
        app.col().sentences.add(note)
        return note

    @classmethod
    def add_sentence(cls, question: str, answer: str, audio: str = "", screenshot: str = "", highlighted_vocab: set[str] | None = None, tags: set[str] | None = None) -> SentenceNote:
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note.source_question.set(question)
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

        app.col().sentences.add(note)
        return note

    @classmethod
    def import_immersion_kit_sentence(cls, immersion_kit_note: Note) -> SentenceNote:
        created = cls.add_sentence(question=immersion_kit_note[ImmersionKitSentenceNoteFields.question],
                                   answer=immersion_kit_note[ImmersionKitSentenceNoteFields.answer],
                                   audio=immersion_kit_note[ImmersionKitSentenceNoteFields.audio],
                                   screenshot=immersion_kit_note[ImmersionKitSentenceNoteFields.screenshot],
                                   tags={Tags.immersion_kit})

        created.id.set(immersion_kit_note[ImmersionKitSentenceNoteFields.id])
        created.reading.set(immersion_kit_note[ImmersionKitSentenceNoteFields.reading])

        return created

    @classmethod
    def create(cls, question: str) -> SentenceNote:
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note.source_question.set(question)
        note.update_generated_data()
        app.col().sentences.add(note)
        return note
