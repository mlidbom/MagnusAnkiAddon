from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import kana_utils

if TYPE_CHECKING:
    from note.sentences.sentence_configuration import SentenceConfiguration
    from note.vocabulary.vocabnote import VocabNote


class CompoundPartViewModel:
    def __init__(self, vocab_note: VocabNote, depth: int, config: SentenceConfiguration) -> None:
        self.vocab_note = vocab_note
        self.depth = depth
        self.question = vocab_note.get_question()
        self.answer = vocab_note.get_answer()
        self.readings = ", ".join(vocab_note.readings.get())
        self.audio_path = vocab_note.audio.get_primary_audio_path()
        self.meta_tags_html: str = vocab_note.meta_data.meta_tags_html(no_sentense_statistics=True)
        self.display_readings = kana_utils.contains_kanji(self.question)
        self.is_highlighted = self.question in config.highlighted_words

        self.meta_tags = " ".join(vocab_note.get_meta_tags())
        self.meta_tags += f""" depth_{depth}"""
        self.meta_tags += " highlighted" if self.is_highlighted else ""
