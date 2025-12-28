from __future__ import annotations

from ankiutils import app
from autoslot import Slots
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.tokenizing.pre_processing_stage.word_info_entry import WordInfoEntry


class WordInfo(Slots):
    @staticmethod
    def lookup(word: str) -> WordInfoEntry | None:
        vocab_entries = app.col().vocab.with_form(word)
        if vocab_entries.any():
            for vocab in vocab_entries:
                if vocab.get_question() == word:
                    return WordInfoEntry(word, vocab.parts_of_speech.get())
            return WordInfoEntry(word, vocab_entries.first().parts_of_speech.get())

        dict_lookup_result = DictLookup.lookup_word(word)
        if dict_lookup_result.found_words():
            return WordInfoEntry(word, dict_lookup_result.parts_of_speech())

        return None

    @staticmethod
    def lookup_godan(word: str) -> WordInfoEntry | None:
        word_info = WordInfo.lookup(word)
        return word_info if word_info is not None and word_info.is_godan else None

    @staticmethod
    def lookup_ichidan(word: str) -> WordInfoEntry | None:
        word_info = WordInfo.lookup(word)
        return word_info if word_info is not None and word_info.is_ichidan else None

    @staticmethod
    def is_godan(word: str) -> bool: return WordInfo.lookup_godan(word) is not None

    @staticmethod
    def is_ichidan(word: str) -> bool: return WordInfo.lookup_ichidan(word) is not None
