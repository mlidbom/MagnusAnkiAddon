# from __future__ import annotations
#
# from autoslot import Slots
# from typed_linq_collections.q_iterable import query
#
# from jaslib import app
# from jaslib.language_services.jamdict_ex.dict_lookup import DictLookup
# from jaslib.language_services.janome_ex.tokenizing.pre_processing_stage.word_info_entry import DictWordInfoEntry, VocabWordInfoEntry, WordInfoEntry
#
#
# class WordInfo(Slots):
#     @classmethod
#     def lookup(cls, word: str) -> WordInfoEntry | None:
#         vocab_entries = query(app.col().vocab.with_form(word))
#         if vocab_entries.any():
#             for vocab in vocab_entries:
#                 if vocab.get_question() == word:
#                     return VocabWordInfoEntry(word, vocab)
#             return VocabWordInfoEntry(word, vocab_entries.first())
#
#         dict_lookup_result = DictLookup.lookup_word(word)
#         if dict_lookup_result.found_words():
#             return DictWordInfoEntry(word, dict_lookup_result)
#
#         return None
#
#     @classmethod
#     def lookup_godan(cls, word: str) -> WordInfoEntry | None:
#         word_info = WordInfo.lookup(word)
#         return word_info if word_info is not None and word_info.is_godan else None
#
#     @classmethod
#     def lookup_ichidan(cls, word: str) -> WordInfoEntry | None:
#         word_info = WordInfo.lookup(word)
#         return word_info if word_info is not None and word_info.is_ichidan else None
#
#     @classmethod
#     def is_godan(cls, word: str) -> bool: return WordInfo.lookup_godan(word) is not None
#
#     @classmethod
#     def is_ichidan(cls, word: str) -> bool: return WordInfo.lookup_ichidan(word) is not None
