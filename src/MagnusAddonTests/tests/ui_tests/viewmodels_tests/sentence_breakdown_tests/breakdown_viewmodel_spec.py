from __future__ import annotations
from viewmodels.sentence_breakdown.sentence_breakdown_viewmodel import VocabHit, BreakDownViewModel, NodeViewModel

from typing import Any, Optional, Union

quad_space = "    "

class VocabHitViewModelSpec:
    def __init__(self, surface_form: str, form: str, hit_form: str, answer: str):
        self.surface_form = surface_form
        self.lookup_form = form
        self.hit_form = hit_form
        self.answer = answer

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, VocabHitViewModelSpec)
                and other.surface_form == self.surface_form
                and other.lookup_form == self.lookup_form
                and other.hit_form == self.hit_form
                and other.answer == self.answer)

    def repr_(self, depth: int) -> str:
        padding = quad_space * depth
        return f"""{padding}V("{self.surface_form}", "{self.lookup_form}", "{self.hit_form}", "{self.answer}")"""

    @staticmethod
    def from_viewmodel(view_model: VocabHit) -> VocabHitViewModelSpec:
        return VocabHitViewModelSpec(view_model.surface_form, view_model.lookup_form, view_model.hit_form, view_model.answer)

class NodeViewModelSpec:
    def __init__(self, surface: str, base: Optional[str], *children: Union[NodeViewModelSpec, VocabHitViewModelSpec]):
        self.surface = surface
        self.base = base
        self.vocab_hits = [surface_hit for surface_hit in children if isinstance(surface_hit, VocabHitViewModelSpec)]
        self.children = [node for node in children if isinstance(node, NodeViewModelSpec)]

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, NodeViewModelSpec)
                and other.surface == self.surface
                and other.base == self.base
                and other.vocab_hits == self.vocab_hits
                and other.children == self.children)

    @classmethod
    def from_view_model(cls, model: NodeViewModel) -> NodeViewModelSpec:
        children = cls.create_children(model.children) if model.children else []
        surface_hits = [VocabHitViewModelSpec.from_viewmodel(sh) for sh in model.surface_vocab_hits]
        base_hits = [VocabHitViewModelSpec.from_viewmodel(bh) for bh in model.base_vocab_hits]
        other = children + surface_hits + base_hits
        return NodeViewModelSpec(model.surface, model.base, *other)

    @classmethod
    def create_children(cls, children: list[NodeViewModel]) -> list[NodeViewModelSpec]:
        return [cls.from_view_model(view_model) for view_model in children]

    def repr_(self, depth: int) -> str:
        padding = quad_space * depth
        return f"""{padding}N("{self.surface}", "{self.base}"{self._repr_vocab_hits(depth)}{self._repr_children(depth)})"""

    def _repr_children(self, depth: int) -> str:
        if not self.children: return ""
        separator = f", \n"
        return f""", \n{separator.join([m.repr_(depth + 1) for m in self.children])}"""

    def _repr_vocab_hits(self, depth: int) -> str:
        if not self.vocab_hits: return ""
        separator = f", \n"
        return f""", \n{separator.join([m.repr_(depth + 1) for m in self.vocab_hits])}"""

class SentenceBreakdownViewModelSpec:
    def __init__(self, *nodes: NodeViewModelSpec):
        self.nodes = list(nodes)

    def __repr__(self) -> str:
        separator = ", \n"
        return f"""SB(
{separator.join([m.repr_(1) for m in self.nodes])})"""

    def repr_single_line(self) -> str:
        return "".join(repr(self).split("\n")).replace(quad_space, "")

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, SentenceBreakdownViewModelSpec)
                and other.nodes == self.nodes)

    @staticmethod
    def from_view_model(model: BreakDownViewModel) -> SentenceBreakdownViewModelSpec:
        return SentenceBreakdownViewModelSpec(*[NodeViewModelSpec.from_view_model(view_model) for view_model in model.nodes])
