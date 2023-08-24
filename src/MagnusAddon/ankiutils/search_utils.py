from wanikani.wani_constants import Wani, Mine

class SearchTags:
    Note = "note"
    Tag = "tag"
    Deck = "deck"
    Card = "card"

def vocab_uk_by_reading(reading: str) -> str: return f"""(tag:_uk AND Reading:{reading})"""

deck_listen = f"{SearchTags.Deck}:{Mine.DeckFilters.Listen}"
kanji_filter = f"{SearchTags.Note}:{Wani.NoteType.Kanji}"
vocab_read = f"({SearchTags.Note}:{Wani.NoteType.Vocab} {SearchTags.Deck}:*Read*)"

def single_vocab_wildcard(vocab:str) -> str: return f"{vocab_read} (Q:*{vocab}* OR Reading:*{vocab}* OR A:*{vocab}*)"