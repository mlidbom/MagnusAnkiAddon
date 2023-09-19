from ankiutils import search_utils
from note.sentencenote import SentenceNote


def build_breakdown_html(sentence: SentenceNote) -> None:
    parsed_words = sentence.get_parsed_words()
    search_utils.text_vocab_lookup(sentence.get_active_question())
