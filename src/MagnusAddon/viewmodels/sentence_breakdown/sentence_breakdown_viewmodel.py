from __future__ import annotations
from note.collection.jp_collection import JPCollection
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode
from language_services.universal_dependencies.shared.tree_building.ud_tree import UDTree

missing_vocab_answer = "---"
class VocabHit:
    def __init__(self, surface_form: str, lookup_form: str, hit_form: str, answer: str):
        self.surface_form = surface_form
        self.lookup_form = lookup_form if lookup_form != surface_form else ""
        self.hit_form = hit_form if hit_form != surface_form and hit_form != lookup_form else ""
        self.answer = answer

    def __repr__(self) -> str: return f"""surface:{self.surface_form} lookup:{self.lookup_form}   hit:{self.hit_form}    answer:{self.answer}"""

    @staticmethod
    def surface_from_vocab(parent: NodeViewModel, vocab: VocabNote) -> VocabHit:
        return VocabHit(surface_form=parent.surface,
                        lookup_form=parent.surface,
                        hit_form=vocab.get_question(),
                        answer=vocab.get_answer())

    @staticmethod
    def base_from_vocab(parent: NodeViewModel, vocab: VocabNote) -> VocabHit:
        return VocabHit(surface_form=parent.surface,
                        lookup_form=parent.base,
                        hit_form=vocab.get_question(),
                        answer=vocab.get_answer())
    @classmethod
    def missing_surface(cls, parent: NodeViewModel) -> VocabHit:
        return VocabHit(surface_form=parent.surface,
                        lookup_form=parent.surface,
                        hit_form=parent.surface,
                        answer=missing_vocab_answer)

    @classmethod
    def missing_base(cls, parent: NodeViewModel) -> VocabHit:
        return VocabHit(surface_form=parent.surface,
                        lookup_form=parent.base,
                        hit_form=parent.base,
                        answer=missing_vocab_answer)

class NodeViewModel:
    def __init__(self, node: UDTreeNode, collection: JPCollection):
        self._node = node
        self._collection = collection
        self.children = [NodeViewModel(nod, collection) for nod in node.children]
        self.surface = self._node.surface
        self.base = node.lemma if node.base_differs_from_surface() else ""
        self.surface_vocab_hits, self.base_vocab_hits = self._vocab_hits()


    def __repr__(self) -> str:
        return f"""surface:{self.surface} base:{self.base}   children:{" # ".join([repr(c) for c in self.children])}"""

    @staticmethod
    def _sort_hits(hits: list[VocabHit]) -> None:
        def question(hit: VocabHit) -> str: return hit.hit_form
        hits.sort(key=question)

    def _vocab_hits(self) -> tuple[list[VocabHit], list[VocabHit]]:
        surface_vocab_notes = self._collection.vocab.with_form(self.surface)

        base_vocab_notes:list[VocabNote] = []
        if self._node.base_should_be_shown_separately_in_breakdown():
            base_vocab_notes = self._collection.vocab.with_form(self.base)

        found_base_vocab = len(base_vocab_notes) > 0
        surface_vocab_ids = set(n.get_id() for n in surface_vocab_notes)
        base_vocab_notes = [b for b in base_vocab_notes if b.get_id() not in surface_vocab_ids]

        surface_vocab = [VocabHit.surface_from_vocab(self, vocab) for vocab in surface_vocab_notes]
        base_vocab = [VocabHit.base_from_vocab(self, vocab) for vocab in base_vocab_notes]


        if not surface_vocab and self._node.is_surface_dictionary_word():
            surface_vocab.append(VocabHit.missing_surface(self))

        if not found_base_vocab and self._node.base_should_be_shown_separately_in_breakdown():
            base_vocab.append(VocabHit.missing_base(self))


        self._sort_hits(surface_vocab)
        self._sort_hits(base_vocab)
        return surface_vocab, base_vocab

class BreakDownViewModel:
    def __init__(self, parse_result: UDTree, collection: JPCollection):
        self._parse_result = parse_result
        self.nodes = [NodeViewModel(node, collection) for node in parse_result.nodes]

def create(sentence: SentenceNote, collection: JPCollection) -> BreakDownViewModel:
    question = sentence.get_question()
    parse_result = ud_tree_builder.build_tree(ud_parsers.best, question)

    return BreakDownViewModel(parse_result, collection)
