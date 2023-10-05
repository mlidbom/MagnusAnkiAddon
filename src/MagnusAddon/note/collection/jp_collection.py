from __future__ import annotations

from anki.collection import Collection

from note.collection.backend_facade import BackEndFacade
from note.collection.kanji_collection import KanjiCollection
from note.collection.radical_collection import RadicalCollection
from note.collection.sentence_collection import SentenceCollection
from note.collection.vocab_collection import VocabCollection
from note.jpnote import JPNote

class JPCollection:
    def __init__(self, anki_collection: Collection):
        backend_facade = BackEndFacade(anki_collection)
        self.anki_collection = anki_collection
        self.vocab = VocabCollection(backend_facade)
        self.kanji = KanjiCollection(backend_facade)
        self.sentences = SentenceCollection(backend_facade)
        self.radicals = RadicalCollection(backend_facade)

    def unsuspend_note_cards(self, note: JPNote, name: str) -> None:
        print("Unsuspending {}: {}".format(JPNote.get_note_type_name(note), name))
        self.anki_collection.sched.unsuspend_cards(note.card_ids())
