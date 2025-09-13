from __future__ import annotations

import typing

from anki.notes import Note
from ankiutils import app
from autoslot import Slots
from note.note_constants import NoteFields, NoteTypes, Tags
from note.notefields.comma_separated_strings_set_field import CommaSeparatedStringsSetField
from note.notefields.string_field import AutoStrippingStringField

if typing.TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef
    from wanikani_api import models  # pyright: ignore[reportMissingTypeStubs]

def create_from_wani_vocabulary(wani_vocab: models.Vocabulary) -> None:
    from note.vocabulary.vocabnote import VocabNote
    note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
    note.add_tag("__imported")
    note.add_tag(Tags.Wani)
    vocab_note = VocabNote(note)
    app.anki_collection().addNote(note)
    vocab_note.question.set(wani_vocab.characters)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

class VocabNoteWaniExtensions(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab
        self._meaning_mnemonic: AutoStrippingStringField = AutoStrippingStringField(vocab, NoteFields.Vocab.source_mnemonic)
        self.component_subject_ids: CommaSeparatedStringsSetField = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.component_subject_ids)
        self.reading_mnemonic: AutoStrippingStringField = AutoStrippingStringField(vocab, NoteFields.Vocab.source_reading_mnemonic)

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def set_source_answer(self, value: str) -> None: self._vocab._source_answer.set(value)  # noqa this extensions is essentially part of the Vocab class  # pyright: ignore[reportPrivateUsage]

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        self._vocab.wani_extensions._meaning_mnemonic.set(wani_vocab.meaning_mnemonic)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

        meanings = ", ".join(str(meaning.meaning) for meaning in wani_vocab.meanings)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
        self.set_source_answer(meanings)

        self.reading_mnemonic.set(wani_vocab.reading_mnemonic)  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

        self._vocab.readings.set([reading.reading for reading in wani_vocab.readings])  # pyright: ignore[reportUnknownMemberType]

        component_subject_ids = {str(subject_id) for subject_id in wani_vocab.component_subject_ids}  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType, reportUnknownMemberType]
        self.component_subject_ids.set(component_subject_ids)
