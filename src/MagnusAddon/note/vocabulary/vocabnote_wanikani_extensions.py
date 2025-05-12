from __future__ import annotations

import typing

from anki.notes import Note
from note.note_constants import Mine, NoteFields, NoteTypes
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField
from note.notefields.comma_separated_strings_set_field import CommaSeparatedStringsSetField
from note.notefields.string_field import StringField
from wanikani.wanikani_api_client import WanikaniClient

if typing.TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from wanikani_api import models

def create_from_wani_vocabulary(wani_vocab: models.Vocabulary) -> None:
    from ankiutils import app
    from note.vocabulary.vocabnote import VocabNote
    note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
    note.add_tag("__imported")
    note.add_tag(Mine.Tags.Wani)
    vocab_note = VocabNote(note)
    app.anki_collection().addNote(note)
    vocab_note.set_question(wani_vocab.characters)
    vocab_note.update_from_wani(wani_vocab)

    if len(wani_vocab.context_sentences) > 0:
        vocab_note.context_sentences.first.english.set(wani_vocab.context_sentences[0].english)
        vocab_note.context_sentences.first.japanese.set(wani_vocab.context_sentences[0].japanese)

    if len(wani_vocab.context_sentences) > 1:
        vocab_note.context_sentences.second.english.set(wani_vocab.context_sentences[1].english)
        vocab_note.context_sentences.second.japanese.set(wani_vocab.context_sentences[1].japanese)

    if len(wani_vocab.context_sentences) > 2:
        vocab_note.context_sentences.third.english.set(wani_vocab.context_sentences[2].english)
        vocab_note.context_sentences.second.japanese.set(wani_vocab.context_sentences[2].japanese)

class VocabNoteWaniExtensions:
    def __init__(self, vocab: VocabNote) -> None:
        self._vocab = vocab
        self._meaning_mnemonic: StringField = StringField(vocab, NoteFields.Vocab.source_mnemonic)
        self.component_subject_ids: CommaSeparatedStringsSetField = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.component_subject_ids)
        self.kanji: CommaSeparatedStringsListField = CommaSeparatedStringsListField(vocab, NoteFields.Vocab.Kanji)
        self.reading_mnemonic: StringField = StringField(vocab, NoteFields.Vocab.source_reading_mnemonic)

    def set_source_answer(self, value: str) -> None: self._vocab._source_answer.set(value) # noqa this extensions is essentially part of the Vocab class

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        self._vocab.wani_extensions._meaning_mnemonic.set(wani_vocab.meaning_mnemonic)

        meanings = ', '.join(str(meaning.meaning) for meaning in wani_vocab.meanings)
        self.set_source_answer(meanings)

        value = ", ".join(wani_vocab.parts_of_speech)
        self._vocab.parts_of_speech.set_raw_string_value(value)

        self.reading_mnemonic.set(wani_vocab.reading_mnemonic)

        self._vocab.readings.set([reading.reading for reading in wani_vocab.readings])

        component_subject_ids = set([str(subject_id) for subject_id in wani_vocab.component_subject_ids])
        self.component_subject_ids.set(component_subject_ids)

        client = WanikaniClient.get_instance()
        kanji_subjects = [client.get_kanji_by_id(int(kanji_id)) for kanji_id in wani_vocab.component_subject_ids]
        kanji_characters = [subject.characters for subject in kanji_subjects]
        self.kanji.set(kanji_characters)