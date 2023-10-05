from __future__ import annotations
from note.collection.jp_collection import JPCollection
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from parsing.universal_dependencies import ud_parsers, ud_tree_builder
from parsing.universal_dependencies.ud_tree_node import UDTextTreeNode
from parsing.universal_dependencies.ud_tree_parse_result import UDTextTree

missing_vocab_answer = "---"
class VocabHit:
    def __init__(self, form: str, hit_form: str, show_hit_form: bool, answer: str):
        self._form = form
        self._hit_form = hit_form
        self._show_hit_form = show_hit_form
        self._answer = answer

    def form(self) -> str: return self._form
    def hit_form(self) -> str: return self._hit_form
    def show_hit_form(self) -> bool: return self._show_hit_form
    def answer(self) -> str: return self._answer

    @staticmethod
    def surface_from_vocab(parent: NodeViewModel, vocab: VocabNote) -> VocabHit:
        return VocabHit(form=parent.surface(),
                        hit_form=vocab.get_question(),
                        show_hit_form=vocab.get_question() != parent.surface(),
                        answer=vocab.get_answer())

    @staticmethod
    def base_from_vocab(parent: NodeViewModel, vocab: VocabNote) -> VocabHit:
        return VocabHit(form=parent.base(),
                        hit_form=vocab.get_question(),
                        show_hit_form=True,
                        answer=vocab.get_answer())
    @classmethod
    def missing_surface(cls, parent: NodeViewModel) -> VocabHit:
        return VocabHit(form=parent.surface(),
                        hit_form="",
                        show_hit_form=False,
                        answer=missing_vocab_answer)

    @classmethod
    def missing_base(cls, parent: NodeViewModel) -> VocabHit:
        return VocabHit(form=parent.base(),
                        hit_form="",
                        show_hit_form=False,
                        answer=missing_vocab_answer)

class NodeViewModel:
    def __init__(self, node: UDTextTreeNode, collection: JPCollection):
        self._node = node
        self._collection = collection
        self.children = [NodeViewModel(nod, collection) for nod in node.children]

    def surface(self) -> str: return self._node.surface
    def base(self) -> str: return self._node.base if self._node.is_inflected() else ""

    def surface_vocab_hits(self) -> list[VocabHit]:
        hits = [VocabHit.surface_from_vocab(self, v) for v in self._collection.vocab.with_form(self.surface())]
        if hits:
            return hits

        if self._node.is_surface_dictionary_word():
            return [VocabHit.missing_surface(self)]

        return []

    def base_vocab_hits(self) -> list[VocabHit]:
        if not self._node.is_inflected(): return []
        hits = [VocabHit.surface_from_vocab(self, v) for v in self._collection.vocab.with_form(self.base())]
        if hits:
            return hits

        if self._node.is_surface_dictionary_word():
            return [VocabHit.missing_base(self)]

        return []

class BreakDownViewModel:
    def __init__(self, parse_result: UDTextTree, collection: JPCollection):
        self._parse_result = parse_result
        self.nodes = [NodeViewModel(node, collection) for node in parse_result.nodes]

def create(sentence: SentenceNote, collection: JPCollection) -> BreakDownViewModel:
    question = sentence.get_question()
    parse_result = ud_tree_builder.build_tree(ud_parsers.best, question)

    return BreakDownViewModel(parse_result, collection)
