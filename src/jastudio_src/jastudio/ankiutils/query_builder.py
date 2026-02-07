from __future__ import annotations

from typing import TYPE_CHECKING

from jaslib.note.note_constants import Builtin, NoteTypes

if TYPE_CHECKING:
    from anki.cards import CardId


note_vocab = f"{Builtin.Note}:{NoteTypes.Vocab}"

note_vocab = note_vocab

def immersion_kit_sentences() -> str:
    return f'''"{Builtin.Note}:{NoteTypes.immersion_kit}"'''

def open_card_by_id(card_id: CardId) -> str:
    return f"cid:{card_id}"


