from anki.cards import *
from anki.consts import QUEUE_TYPE_NEW
from aqt import mw

from wanikani.Note.MyNote import MyNote
from wanikani.Note.SentenceNote import SentenceNote
from wanikani.Note.WaniKanjiNote import WaniKanjiNote
from wanikani.Note.WaniNote import WaniNote
from wanikani.Note.WaniRadicalNote import WaniRadicalNote
from wanikani.Note.WaniVocabNote import WaniVocabNote
from wanikani.wani_constants import Wani


class NoteUtils:
    @staticmethod
    def get_note_type(note: Note) -> str:
        return note.note_type()["name"]

    @staticmethod
    def create_note(card: Card) -> MyNote:
        note = card.note()
        if NoteUtils.get_note_type(note) == Wani.NoteType.Kanji:
            return WaniKanjiNote(note)
        elif NoteUtils.get_note_type(note) == Wani.NoteType.Vocab:
            return WaniVocabNote(note)
        elif NoteUtils.get_note_type(note) == Wani.NoteType.Radical:
            return WaniRadicalNote(note)
        else:
            deck = mw.col.decks.get(card.current_deck_id())
            if "sentence" in deck['name'].lower():
                return SentenceNote(note)
        return MyNote(note)


class CardUtils:
    @staticmethod
    def is_new(card: Card) -> bool:
        return card.queue == QUEUE_TYPE_NEW

    @classmethod
    def get_note_type_priority(cls, card: Card):
        note_type_name = card.note_type()["name"]
        if note_type_name == Wani.NoteType.Radical: return 1
        if note_type_name == Wani.NoteType.Kanji: return 2
        if note_type_name == Wani.NoteType.Vocab: return 3

        return 4  # It's nice to use it for other note types too so default them to 4.

    @classmethod
    def prioritize(cls, card: Card):
        if CardUtils.is_new(card):
            card.due = cls.get_note_type_priority(card)
            card.flush()

    @classmethod
    def prioritize_note_cards(cls, note: WaniNote, name: str):
        cards = [mw.col.get_card(card_id) for card_id in note.card_ids()]
        for card in cards:
            print("Prioritizing {}: {}".format(WaniNote.get_note_type_name(note), name))
            CardUtils.prioritize(card)

    @classmethod
    def answer_again_with_zero_interval_for_new_note_cards(cls, note: WaniNote, name: str):
        cards = [mw.col.get_card(card_id) for card_id in note.card_ids()]
        for card in cards:
            if CardUtils.is_new(card):
                print("Answering new card again {}: {}".format(WaniNote.get_note_type_name(note), name))
                card.start_timer()  # answerCard crashes unless I do this.
                mw.col.sched.answerCard(card, 1)
                card.due = int(time.time())
                card.flush()
