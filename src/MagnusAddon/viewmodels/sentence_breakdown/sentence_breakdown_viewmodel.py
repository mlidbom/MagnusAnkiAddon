from __future__ import annotations

from language_services.shared import priorities
from language_services.universal_dependencies.shared.tree_building.ud_tree import UDTree
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode
from note.collection.jp_collection import JPCollection
from note.vocabnote import VocabNote
from sysutils import kana_utils

missing_vocab_answer = "---"
class VocabHit:
    def __init__(self, surface_form: str, lookup_form: str, hit_form: str, answer: str, readings:list[str], meta_tags:str,  meta_tags_html: str):
        self.surface_form = surface_form
        self.lookup_form = lookup_form if lookup_form != surface_form else ""
        self.hit_form = hit_form if hit_form != surface_form and hit_form != lookup_form else ""
        self.answer = answer
        self.readings = readings
        self.meta_tags = meta_tags
        self.meta_tags_html = meta_tags_html

    def __repr__(self) -> str: return f"""surface:{self.surface_form} lookup:{self.lookup_form}   hit:{self.hit_form}    answer:{self.answer}"""

    @staticmethod
    def surface_from_vocab(parent: NodeViewModel, vocab: VocabNote) -> VocabHit:
        return VocabHit(surface_form=parent.surface,
                        lookup_form=parent.surface,
                        hit_form=vocab.get_question(),
                        answer=vocab.get_answer(),
                        readings=vocab.get_readings(),
                        meta_tags=vocab.get_meta_tags(),
                        meta_tags_html=vocab.get_meta_tags_html())

    @staticmethod
    def base_from_vocab(parent: NodeViewModel, vocab: VocabNote) -> VocabHit:
        return VocabHit(surface_form=parent.surface,
                        lookup_form=parent.base,
                        hit_form=vocab.get_question(),
                        answer=vocab.get_answer(),
                        readings=vocab.get_readings(),
                        meta_tags=vocab.get_meta_tags(),
                        meta_tags_html=vocab.get_meta_tags_html())
    @classmethod
    def missing_surface(cls, parent: NodeViewModel) -> VocabHit:
        return VocabHit(surface_form=parent.surface,
                        lookup_form=parent.surface,
                        hit_form=parent.surface,
                        answer=missing_vocab_answer,
                        readings=[],
                        meta_tags="",
                        meta_tags_html="")

    @classmethod
    def missing_base(cls, parent: NodeViewModel) -> VocabHit:
        return VocabHit(surface_form=parent.surface,
                        lookup_form=parent.base,
                        hit_form=parent.base,
                        answer=missing_vocab_answer,
                        readings=[],
                        meta_tags="",
                        meta_tags_html="")

class NodeViewModel:
    def __init__(self, node: UDTreeNode, collection: JPCollection):
        self._node = node
        self._collection = collection
        self.children = [NodeViewModel(nod, collection) for nod in node.children]
        self.surface = self._node.form
        self.base = node.lemma if node.lemma_differs_from_form() else ""
        self.surface_vocab_hits, self.base_vocab_hits = self._vocab_hits()


    def __repr__(self) -> str:
        return f"""surface:{self.surface} base:{self.base}   children:{" # ".join([repr(c) for c in self.children])}"""

    @staticmethod
    def _sort_hits(hits: list[VocabHit]) -> None:
        def question(hit: VocabHit) -> str: return hit.hit_form
        hits.sort(key=question)

    def _vocab_hits(self) -> tuple[list[VocabHit], list[VocabHit]]:

        form_vocab_notes:list[VocabNote] = self._collection.vocab.with_form(self.surface) if not self._node.form_should_be_excluded_from_breakdown() else []

        base_vocab_notes:list[VocabNote] = []
        if self._node.lemma_should_be_shown_in_breakdown():
            base_vocab_notes = self._collection.vocab.with_form(self.base)

        found_base_vocab = len(base_vocab_notes) > 0
        surface_vocab_ids = set(n.get_id() for n in form_vocab_notes)
        base_vocab_notes = [b for b in base_vocab_notes if b.get_id() not in surface_vocab_ids]

        surface_vocab = [VocabHit.surface_from_vocab(self, vocab) for vocab in form_vocab_notes]
        base_vocab = [VocabHit.base_from_vocab(self, vocab) for vocab in base_vocab_notes]


        if not surface_vocab and self._node.form_is_required_in_breakdown():
            surface_vocab.append(VocabHit.missing_surface(self))

        if not found_base_vocab and self._node.lemma_should_be_shown_in_breakdown():
            base_vocab.append(VocabHit.missing_base(self))


        self._sort_hits(surface_vocab)
        self._sort_hits(base_vocab)
        return surface_vocab, base_vocab

    def get_priority_class(self, question: str, highlighted: set[str]) -> str:
        if question in highlighted:
            return priorities.very_high

        if question != self.surface and question != self.base:
            return priorities.unknown

        kanji_count = len([char for char in self.surface if kana_utils.is_kanji(char)])
        katakana_count = len([char for char in self.surface if kana_utils.is_katakana(char)])

        # todo: if this works out well, remove the code with hard coded values below
        if kanji_count == 0 and katakana_count == 0:
            if len(self.surface) == 1:
                return priorities.very_low
            if len(self.surface) == 2:
                return priorities.low

        if question == self.surface:
            if question in priorities.hard_coded_surface_priorities:
                return priorities.hard_coded_surface_priorities[question]
        if question == self.base:
            if question in priorities.hard_coded_base_priorities:
                return priorities.hard_coded_base_priorities[question]

        if kanji_count > 1:
            return priorities.high

        return priorities.medium

class BreakDownViewModel:
    def __init__(self, parse_result: UDTree, collection: JPCollection):
        self._parse_result = parse_result
        self.nodes = [NodeViewModel(node, collection) for node in parse_result.nodes]

def create(tree: UDTree, collection: JPCollection) -> BreakDownViewModel:
    return BreakDownViewModel(tree, collection)
