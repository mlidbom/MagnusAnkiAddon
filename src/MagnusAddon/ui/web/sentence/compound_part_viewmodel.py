from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from ex_autoslot import ProfilableAutoSlots
from sysutils import ex_sequence

if TYPE_CHECKING:
    from anki.notes import NoteId
    from note.sentences.sentence_configuration import SentenceConfiguration
    from note.vocabulary.vocabnote import VocabNote

class CompoundPartViewModel(ProfilableAutoSlots):
    def __init__(self, vocab_note: VocabNote, depth: int, config: SentenceConfiguration) -> None:
        self.vocab_note: VocabNote = vocab_note
        self.depth: int = depth
        self.question: str = vocab_note.get_question()
        self.answer: str = vocab_note.get_answer()
        self.readings: str = ", ".join(vocab_note.readings.get())
        self.audio_path: str = vocab_note.audio.get_primary_audio_path()
        self.meta_tags_html: str = vocab_note.meta_data.meta_tags_html(no_sentense_statistics=True)
        self.display_readings: bool = self.question != self.readings
        self.is_highlighted: bool = self.question in config.highlighted_words

        self.meta_tags_string: str = " ".join(vocab_note.get_meta_tags())
        self.meta_tags_string += f""" depth_{depth}"""
        self.meta_tags_string += " highlighted" if self.is_highlighted else ""

    @classmethod
    def get_compound_parts_recursive(cls, vocab_note: VocabNote, config: SentenceConfiguration, depth: int = 0, visited: set[NoteId] | None = None) -> list[CompoundPartViewModel]:
        if not app.config().show_compound_parts_in_sentence_breakdown.get_value(): return []
        if visited is None: visited = set()
        if vocab_note.get_id() in visited: return []

        visited.add(vocab_note.get_id())

        compound_parts = ex_sequence.flatten([app.col().vocab.with_form_prefer_exact_match(part) for part in vocab_note.compound_parts.primary()])

        result: list[CompoundPartViewModel] = []

        for part in compound_parts:
            wrapper = CompoundPartViewModel(part, depth, config)
            result.append(wrapper)
            nested_parts = cls.get_compound_parts_recursive(part, config, depth + 1, visited)
            result.extend(nested_parts)

        return result
