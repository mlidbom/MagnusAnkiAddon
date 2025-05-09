from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.sentencenote_configuration import SentenceConfiguration
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
        self._user_excluded_cache:set[str] = self._get_user_word_exclusions_strings()


    def get_direct_dependencies(self) -> set[JPNote]:
        highlighted = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.get_user_highlighted_vocab()]))
        valid_parsed_roots = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.get_valid_parsed_non_child_words_strings()]))
        kanji = set(self.collection.kanji.with_any_kanji_in(self.extract_kanji()))
        return highlighted | valid_parsed_roots | kanji

    def get_question(self) -> str: return self._get_user_question() or self._get_source_question()
    def get_answer(self) -> str: return self._get_user_answer() or self._get_source_answer()

    def _get_source_answer(self) -> str: return self.get_field(SentenceNoteFields.source_answer)
    def _set_source_answer(self, question: str) -> None: return self.set_field(SentenceNoteFields.source_answer, question)

    def _set_screenshot(self, screenshot: str) -> None: return self.set_field(SentenceNoteFields.screenshot, screenshot)

    def _set_audio(self, audio: str) -> None: return self.set_field(SentenceNoteFields.audio, audio)

    def _get_user_answer(self) -> str: return self.get_field(SentenceNoteFields.user_answer)

    def _set_user_answer(self, question: str) -> None: return self.set_field(SentenceNoteFields.user_answer, question)

    def _get_source_question(self) -> str: return ex_str.strip_html_markup(self.get_field(SentenceNoteFields.source_question)).strip()
    def _set_source_question(self, question: str) -> None: return self.set_field(SentenceNoteFields.source_question, question)

    def _get_user_question(self) -> str: return ex_str.strip_html_markup(self.get_field(SentenceNoteFields.user_question)).strip()

    def get_audio_path(self) -> str: return ex_str.strip_html_markup(self.get_field(SentenceNoteFields.audio)).strip()[7:-1]

    def get_user_excluded_vocab(self) -> set[str]: return self._user_excluded_cache

    def get_user_word_exclusions(self) -> list[WordExclusion]:
        strings = ex_str.extract_newline_separated_values(self.get_field(SentenceNoteFields.user_excluded_vocab))
        return [WordExclusion.from_string(s) for s in strings]

    def _get_user_word_exclusions_strings(self) -> set[str]:
        word_exclusions = set(x.word for x in self.get_user_word_exclusions())
        valid_words = set(self.get_parsed_words())
        return word_exclusions - valid_words

    def _set_user_word_exclusions(self, exclusions: set[WordExclusion]) -> None:
        sorted_exclusions = sorted(exclusions, key=lambda x: x.index)
        self.set_field(SentenceNoteFields.user_excluded_vocab, newline.join([e.as_string() for e in sorted_exclusions]))
        self.update_parsed_words(force=True)
        self._user_excluded_cache = self._get_user_word_exclusions_strings()

    def is_studying_read(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Reading)
    def is_studying_listening(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Listening)


    def get_valid_parsed_non_child_words_strings(self) -> list[str]:
        return [w.form for w in self.get_valid_parsed_non_child_words()]

    def get_valid_parsed_non_child_words(self) -> list[CandidateForm]:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        analysis = TextAnalysis(self.get_question(), list(self.get_user_word_exclusions()))
        return analysis.display_words

    def get_user_highlighted_vocab(self) -> list[str]: return ex_str.extract_newline_separated_values(self.get_field(SentenceNoteFields.user_extra_vocab))
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
        self._set_user_extra_vocab([v for v in self.get_user_highlighted_vocab() if not v == vocab])

    def reset_highlighted(self) -> None:
        self._set_user_extra_vocab([])

    def reset_excluded(self) -> None:
        self._set_user_word_exclusions(set())

    def remove_excluded_vocab(self, vocab: str) -> None:
        exclusion = WordExclusion.from_string(vocab)
        excluded = self.get_user_word_exclusions()
        new_excluded = {e for e in excluded if not exclusion.covers(e)}
        self._set_user_word_exclusions(new_excluded)

    def exclude_vocab(self, vocab: str) -> None:
        exclusion = WordExclusion.from_string(vocab)
        self.remove_extra_vocab(exclusion.word)
        excluded = set(self.get_user_word_exclusions())
        excluded.add(exclusion)
        self._set_user_word_exclusions(excluded)

    def parse_words_from_expression(self) -> list[ExtractedWord]:
        from language_services.janome_ex.word_extraction.word_extractor import jn_extractor
        return jn_extractor.extract_words(self.get_question())

    def get_parsed_words(self) -> list[str]: return self._get_parsed_words()[:-1]
    def _get_parsed_words(self) -> list[str]: return self.get_field(SentenceNoteFields.ParsedWords).split(",")
    def get_words(self) -> set[str]: return (set(self._get_parsed_words()) | set(self.get_user_highlighted_vocab())) - self.get_user_excluded_vocab()

    def get_parsed_words_notes(self) -> list[VocabNote]:
        from ankiutils import app
        return ex_sequence.flatten([app.col().vocab.with_question(q) for q in self.get_valid_parsed_non_child_words_strings()])


    def update_generated_data(self) -> None:
        super().update_generated_data()
        self.update_parsed_words()
        self.set_field(SentenceNoteFields.active_answer, self.get_answer())
        self.set_field(SentenceNoteFields.active_question, self.get_question())

        config = self.get_configuration()

    def update_parsed_words(self, force:bool = False) -> None:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        words = self._get_parsed_words()
        old_parsed_sentence = words[-1] if words else ""
        current_storable_sentence = f"""{self.get_question().replace(",", "").strip()}-parser_version-{TextAnalysis.version}"""

        if force or old_parsed_sentence != current_storable_sentence:
            analysis = TextAnalysis(self.get_question(), list(self.get_user_word_exclusions()))
            value = [parsed_word.form for parsed_word in analysis.all_words]
            value.append(current_storable_sentence)
            self.set_field(SentenceNoteFields.ParsedWords, ",".join(value))


    def extract_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    @classmethod
    def create_test_note(cls, question: str, answer: str) -> SentenceNote:
        from ankiutils import app
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._set_source_question(question)
        note._set_user_answer(answer)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note

    @classmethod
    def add_sentence(cls, question: str, answer:str, audio:str = "", screenshot:str = "", highlighted_vocab: Optional[set[str]] = None, tags: Optional[set[str]] = None) -> SentenceNote:
        from ankiutils import app
        inner_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        note = SentenceNote(inner_note)
        note._set_source_question(question)
        note._set_source_answer(answer)
        note._set_screenshot(screenshot)
        note.update_generated_data()

        if not audio.strip():
            note.set_tag(Mine.Tags.TTSAudio)
        else:
            note._set_audio(audio.strip())

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
        note._set_source_question(question)
        note.update_generated_data()
        app.anki_collection().addNote(inner_note)
        return note



    def get_configuration(self) -> SentenceConfiguration:
        config_json = self.get_field(SentenceNoteFields.configuration)
        if not config_json:
            # Generate configuration from existing fields for backward compatibility
            config = SentenceConfiguration(
                highlighted_words=self.get_user_highlighted_vocab(),
                word_exclusions=self.get_user_word_exclusions()
            )
            self.set_configuration(config)
            return config

        return SentenceConfiguration.from_json(config_json)

    def set_configuration(self, config: SentenceConfiguration) -> None:
        config_json = config.to_json()
        self.set_field(SentenceNoteFields.configuration, config_json)


    def add_highlighted_word_to_config(self, word: str, index: int = -1) -> None:
        config = self.get_configuration()
        if word in config.highlighted_words:
            config.highlighted_words.remove(word)

        if index == -1:
            config.highlighted_words.append(word)
        else:
            config.highlighted_words.insert(index, word)

        self.set_configuration(config)

    def remove_highlighted_word_from_config(self, word: str) -> None:
        config = self.get_configuration()

        if word in config.highlighted_words:
            config.highlighted_words.remove(word)
            self.set_configuration(config)

    def add_word_exclusion_to_config(self, exclusion: WordExclusion) -> None:
        config = self.get_configuration()

        config.word_exclusions = [e for e in config.word_exclusions if e.word != exclusion.word]
        config.word_exclusions.append(exclusion)
        self.set_configuration(config)

    def remove_word_exclusion_from_config(self, word: str) -> None:
        config = self.get_configuration()

        config.word_exclusions = [e for e in config.word_exclusions
                                  if e.word != word]

        self.set_configuration(config)

    def reset_highlighted_in_config(self) -> None:
        config = self.get_configuration()
        config.highlighted_words = []
        self.set_configuration(config)

    def reset_exclusions_in_config(self) -> None:
        config = self.get_configuration()
        config.word_exclusions = []
        self.set_configuration(config)