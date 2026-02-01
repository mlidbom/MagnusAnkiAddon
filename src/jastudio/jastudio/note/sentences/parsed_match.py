from __future__ import annotations

from typing import TYPE_CHECKING, override

from anki.notes import NoteId
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.note.sentences.serialization.parsed_word_serializer import ParsedWordSerializer
from sysutils.memory_usage import string_auto_interner

from jastudio.language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.match import Match

class ParsedMatch(Slots):
    missing_note_id:NoteId = NoteId(-1)
    serializer: ParsedWordSerializer = ParsedWordSerializer()
    def __init__(self, variant: str, start_index: int, is_displayed: bool, word: str, vocab_id: NoteId) -> None:
        self.start_index: int = start_index
        self.is_displayed: bool = is_displayed
        self.variant: str = string_auto_interner.auto_intern(variant)
        self.parsed_form: str = string_auto_interner.auto_intern(word)
        self.vocab_id: NoteId = vocab_id

    @property
    def end_index(self) -> int: return self.start_index + len(self.parsed_form)

    @classmethod
    def from_match(cls, match: Match) -> ParsedMatch:
        return ParsedMatch("S" if match.variant.is_surface else "B",
                           match.start_index,
                           match.is_valid_for_display,
                           match.parsed_form,
                           match.vocab.get_id() if isinstance(match, VocabMatch) else cls.missing_note_id)

    @override
    def __repr__(self) -> str: return self.serializer.to_row(self)