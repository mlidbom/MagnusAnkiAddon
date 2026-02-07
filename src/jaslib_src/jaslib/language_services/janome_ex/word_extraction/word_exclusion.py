# from __future__ import annotations
#
# from typing import TYPE_CHECKING, final, override
#
# from autoslot import Slots
# from typed_linq_collections.collections.q_dict import QDict
#
# from jaslib.note.vocabulary.vocabnote_question import VocabNoteQuestion
#
# if TYPE_CHECKING:
#     from jaspythonutils.sysutils.json.json_reader import JsonReader
#
#
#
# @final
# class WordExclusion(Slots):
#     secret = "aoesunth9cgrcgf"
#     _no_index = -1
#     def __init__(self, word: str, index: int, _secret: str) -> None:
#         if _secret != "aoesunth9cgrcgf": raise ValueError("please use the factory methods instead of this private constructor")
#         self.word = word
#         self.index = index
#         self._match_part = word.split(VocabNoteQuestion.DISAMBIGUATION_MARKER)[0]
#
#     def excludes_form_at_index(self, form: str, index: int) -> bool:
#         return form == self.word and (self.index == WordExclusion._no_index or self.index == index)
#
#     @classmethod
#     def global_(cls, exclusion: str) -> WordExclusion: return WordExclusion(exclusion.strip(), WordExclusion._no_index, WordExclusion.secret)
#     @classmethod
#     def at_index(cls, exclusion: str, index: int) -> WordExclusion: return WordExclusion(exclusion.strip(), index, WordExclusion.secret)
#
#     @override
#     def __eq__(self, other: object) -> bool:
#         if isinstance(other, WordExclusion):
#             return self.word == other.word and self.index == other.index
#         return False
#
#     @override
#     def __hash__(self) -> int:
#         return hash((self.word, self.index))
#
#     @override
#     def __repr__(self) -> str:
#         return f"WordExclusion('{self.word}', {self.index})"
#
#     # noinspection PyUnusedFunction
#     def excludes_all_words_excluded_by(self, other: WordExclusion) -> bool:
#         return self.word == other.word and (self.index == WordExclusion._no_index or self.index == other.index)
#
#     def to_dict(self) -> QDict[str, object]:
#         return QDict({"word": self.word, "index": self.index})
#
#     @classmethod
#     def from_reader(cls, reader: JsonReader) -> WordExclusion:
#         return cls(word=reader.string("word"), index=reader.integer("index"), _secret=WordExclusion.secret)
