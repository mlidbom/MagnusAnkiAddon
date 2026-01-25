from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from anki.notes import Note
from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.jpnote import JPNote
from note.note_constants import ImmersionKitSentenceNoteFields, NoteFields, NoteTypes, SentenceNoteFields
from note.notefields.audio_field import WritableAudioField
from note.notefields.json_object_field import MutableSerializedObjectField
from note.notefields.mutable_string_field import MutableStringField
from note.notefields.sentence_question_field import SentenceQuestionField
from note.notefields.strip_html_on_read_fallback_string_field import StripHtmlOnReadFallbackStringField
from note.sentences.caching_sentence_configuration_field import CachingSentenceConfigurationField
from note.sentences.parsing_result import ParsingResult
from note.sentences.user_fields import SentenceUserFields
from note.tags import Tags
from sysutils import ex_str, kana_utils
from sysutils.weak_ref import WeakRef
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from note.tag import Tag
    from note.vocabulary.vocabnote import VocabNote
    from typed_linq_collections.collections.q_list import QList
    from typed_linq_collections.collections.q_unique_list import QUniqueList

class SentenceNote(JPNote, Slots):
    def __init__(self, note: Note) -> None:
        super().__init__(note)
        self.weakref_sentence: WeakRef[SentenceNote] = cast(WeakRef[SentenceNote], self.weakref)

        self.configuration: CachingSentenceConfigurationField = CachingSentenceConfigurationField(self.weakref_sentence)
        self.parsing_result: MutableSerializedObjectField[ParsingResult] = MutableSerializedObjectField[ParsingResult](self.weakref, SentenceNoteFields.parsing_result, ParsingResult.serializer)


    @property
    def id(self) -> MutableStringField: return MutableStringField(self.weakref, SentenceNoteFields.id)
    @property
    def reading(self) -> MutableStringField: return MutableStringField(self.weakref, SentenceNoteFields.reading)
    @property
    def user(self) -> SentenceUserFields: return SentenceUserFields(self.weakref_sentence)
    @property
    def source_question(self) -> MutableStringField: return MutableStringField(self.weakref, SentenceNoteFields.source_question)
    @property
    def active_question(self) -> MutableStringField: return MutableStringField(self.weakref, SentenceNoteFields.active_question)
    @property
    def question(self) -> SentenceQuestionField: return SentenceQuestionField(self.user.question, self.source_question)
    @property
    def answer(self) -> StripHtmlOnReadFallbackStringField: return StripHtmlOnReadFallbackStringField(self.user.answer, self._source_answer)
    @property
    def _source_answer(self) -> MutableStringField: return MutableStringField(self.weakref, SentenceNoteFields.source_answer)
    @property
    def active_answer(self) -> MutableStringField: return MutableStringField(self.weakref, SentenceNoteFields.active_answer)
    @property
    def source_comments(self) -> MutableStringField: return MutableStringField(self.weakref, SentenceNoteFields.source_comments)
    @property
    def _screenshot(self) -> MutableStringField: return MutableStringField(self.weakref, SentenceNoteFields.screenshot)
    @property
    def audio(self) -> WritableAudioField: return WritableAudioField(self.weakref, SentenceNoteFields.audio)

    @override
    def get_question(self) -> str: return self.question.with_invisible_space()
    @override
    def get_answer(self) -> str: return self.answer.get()

    def is_studying_read(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Reading)
    def is_studying_listening(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Listening)

    def get_valid_parsed_non_child_words_strings(self) -> QList[str]:
        return self.get_valid_parsed_non_child_words().select(lambda word: word.form).to_list()  #[w.form for w in self.get_valid_parsed_non_child_words()]

    def get_valid_parsed_non_child_words(self) -> QList[CandidateWordVariant]:
        return self.create_analysis().display_word_variants

    def create_analysis(self, for_ui: bool = False) -> TextAnalysis:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        return TextAnalysis(self.question.with_invisible_space(), self.configuration.configuration, for_ui=for_ui)

    @override
    def get_direct_dependencies(self) -> QSet[JPNote]:
        highlighted = self.configuration.highlighted_vocab
        displayed_vocab = (voc for voc in {app.col().vocab.with_id_or_none(voc.vocab_id)
                                           for voc in self.parsing_result.get().parsed_words
                                           if voc.is_displayed}
                           if voc is not None)
        kanji = self.collection.kanji.with_any_kanji_in(self.extract_kanji())
        return QSet.create(highlighted, displayed_vocab, kanji)

    def get_words(self) -> QUniqueList[str]: return (self.parsing_result.get().parsed_words_strings() | self.configuration.highlighted_words()) - self.configuration.incorrect_matches.words()

    def get_parsed_words_notes(self) -> list[VocabNote]:
        return (self.get_valid_parsed_non_child_words_strings()
                .select_many(app.col().vocab.with_question).to_list()) #ex_sequence.flatten([app.col().vocab.with_question(q) for q in self.get_valid_parsed_non_child_words_strings()])

    @override
    def update_generated_data(self) -> None:
        super().update_generated_data()
        self.update_parsed_words()
        self.active_answer.set(self.get_answer())
        self.active_question.set(self.question.with_invisible_space()) #todo should this be with the invisible space?

    def update_parsed_words(self, force: bool = False) -> None:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        parsing_result = self.parsing_result.get()
        if not force and parsing_result and parsing_result.sentence == self.question.without_invisible_space() and parsing_result.parser_version == TextAnalysis.version:
            return

        analysis = self.create_analysis()
        self.parsing_result.set(ParsingResult.from_analysis(analysis))

    def extract_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.question.without_invisible_space())
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
    def add_sentence(cls, question: str, answer: str, audio: str = "", screenshot: str = "", highlighted_vocab: QSet[str] | None = None, tags: QSet[Tag] | None = None) -> SentenceNote:
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note.source_question.set(question)
        note._source_answer.set(answer)
        note._screenshot.set(screenshot)
        note.update_generated_data()

        if not audio.strip():
            note.tags.set(Tags.TTSAudio)
        else:
            audio1 = audio.strip()
            note.audio.set_raw_value(audio1)

        if highlighted_vocab:
            for vocab in highlighted_vocab:
                note.configuration.add_highlighted_word(vocab)

        if tags:
            for tag in tags:
                note.tags.set(tag)

        app.col().sentences.add(note)
        return note

    @classmethod
    def import_immersion_kit_sentence(cls, immersion_kit_note: Note) -> SentenceNote:
        created = cls.add_sentence(question=immersion_kit_note[ImmersionKitSentenceNoteFields.question],
                                   answer=immersion_kit_note[ImmersionKitSentenceNoteFields.answer],
                                   audio=immersion_kit_note[ImmersionKitSentenceNoteFields.audio],
                                   screenshot=immersion_kit_note[ImmersionKitSentenceNoteFields.screenshot],
                                   tags=QSet([Tags.Source.immersion_kit]))

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
