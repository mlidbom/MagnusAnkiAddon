from __future__ import annotations

import typing

from anki.notes import Note
from note.note_constants import Mine, NoteTypes
from wanikani.wanikani_api_client import WanikaniClient

if typing.TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from wanikani_api import models

def update_from_wani(self: VocabNote, wani_vocab: models.Vocabulary) -> None:
    self.set_meaning_mnemonic(wani_vocab.meaning_mnemonic)

    meanings = ', '.join(str(meaning.meaning) for meaning in wani_vocab.meanings)
    self._set_source_answer(meanings)

    value = ", ".join(wani_vocab.parts_of_speech)
    self.parts_of_speech.set_raw_string_value(value)

    self.set_reading_mnemonic(wani_vocab.reading_mnemonic)

    self.readings.set([reading.reading for reading in wani_vocab.readings])

    component_subject_ids = [str(subject_id) for subject_id in wani_vocab.component_subject_ids]
    self.set_component_subject_ids(", ".join(component_subject_ids))

    client = WanikaniClient.get_instance()
    kanji_subjects = [client.get_kanji_by_id(int(kanji_id)) for kanji_id in wani_vocab.component_subject_ids]
    kanji_characters = [subject.characters for subject in kanji_subjects]
    self.set_kanji(", ".join(kanji_characters))

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
