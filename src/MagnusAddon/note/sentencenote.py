from __future__ import annotations
from typing import Optional, TYPE_CHECKING

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
        self._user_excluded_cache:set[str] = set(ex_str.extract_newline_separated_values(self.get_field(SentenceNoteFields.user_excluded_vocab)))


    def get_direct_dependencies(self) -> set[JPNote]:
        highlighted = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.get_user_highlighted_vocab()]))
        valid_parsed_roots = set(ex_sequence.flatten([self.collection.vocab.with_question(vocab) for vocab in self.get_valid_parsed_non_child_words()]))
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
    def _set_user_excluded_vocab(self, excluded: set[str]) -> None:
        self._user_excluded_cache = excluded
        self.set_field(SentenceNoteFields.user_excluded_vocab, newline.join(self._user_excluded_cache))


    def is_studying_read(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Reading)
    def is_studying_listening(self) -> bool: return self.is_studying(NoteFields.SentencesNoteType.Card.Listening)


    def get_valid_parsed_non_child_words(self) -> list[str]:
        from language_services.janome_ex.word_extraction import word_extractor
        roots = word_extractor.extract_words_hierarchical(self.get_question(), self.get_user_excluded_vocab())

        return [w.word.word for w in roots]

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

    def remove_excluded_vocab(self, vocab: str) -> None:
        excluded = self.get_user_excluded_vocab()
        if vocab in excluded:
            excluded.remove(vocab.strip())

        self._set_user_excluded_vocab(excluded)

    def exclude_vocab(self, vocab: str) -> None:
        self.remove_extra_vocab(vocab)
        excluded = self.get_user_excluded_vocab()
        excluded.add(vocab.strip())
        self._set_user_excluded_vocab(excluded)

    def parse_words_from_expression(self) -> list[ExtractedWord]:
        from language_services.janome_ex.word_extraction import word_extractor
        return word_extractor.extract_words(self.get_question())

    def ud_extract_word_forms(self) -> list[str]:
        from language_services.universal_dependencies import ud_tokenizers
        from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
        from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode

        tree = ud_tree_builder.build_tree(ud_tokenizers.default, self.get_question())
        word_forms: set[str] = set()

        def get_node_forms(node: UDTreeNode) -> None:
            word_forms.add(node.form)
            if node.lemma_should_be_shown_in_breakdown():
                word_forms.add(node.lemma)

        tree.visit(get_node_forms)

        return list(word_forms)

    def ud_extract_vocab(self) -> list[VocabNote]:
        from ankiutils import app
        return app.col().vocab.with_forms(self.ud_extract_word_forms())

    def get_parsed_words(self) -> list[str]: return self._get_parsed_words()[:-1]
    def _get_parsed_words(self) -> list[str]: return self.get_field(SentenceNoteFields.ParsedWords).split(",")
    def get_words(self) -> set[str]: return (set(self._get_parsed_words()) | set(self.get_user_highlighted_vocab())) - self.get_user_excluded_vocab()

    def update_generated_data(self) -> None:
        super().update_generated_data()
        self.update_parsed_words()
        self.set_field(SentenceNoteFields.active_answer, self.get_answer())
        self.set_field(SentenceNoteFields.active_question, self.get_question())

    def update_parsed_words(self, force:bool = False) -> None:
        from language_services.janome_ex.word_extraction import word_extractor
        words = self._get_parsed_words()
        old_parsed_sentence = words[-1] if words else ""
        current_storable_sentence = f"""{self.get_question().replace(",", "").strip()}-parser_version-{word_extractor.version}"""

        if force or old_parsed_sentence != current_storable_sentence:
            value = [parsed_word.word for parsed_word in word_extractor.extract_words(self.get_question())]
            value.append(current_storable_sentence)
            self.set_field(SentenceNoteFields.ParsedWords, ",".join(value))


    def extract_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.is_kanji(char)]

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