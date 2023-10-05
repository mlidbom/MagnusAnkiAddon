from __future__ import annotations

from typing import Any

from sysutils.ex_str import full_width_space, newline
from viewmodels.sentence_breakdown.sentence_breakdown_viewmodel import BreakDownViewModel, NodeViewModel

class NodeViewModelSpec:
    def __init__(self, surface: str, base: str | None, *children: NodeViewModelSpec):
        self.surface = surface
        self.base = base
        self.children = list(children)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, NodeViewModelSpec)
                and other.surface == self.surface
                and other.base == self.base
                and other.children == self.children)

    @classmethod
    def from_view_model(cls, model: NodeViewModel) -> NodeViewModelSpec:
        children: list[NodeViewModelSpec] = cls.create_children(model.children) if model.children else []
        return NodeViewModelSpec(model.surface(), model.base(), *children)

    @classmethod
    def create_children(cls, children: list[NodeViewModel]) -> list[NodeViewModelSpec]:
        return [cls.from_view_model(view_model) for view_model in children]

    def repr_(self, depth: int) -> str:
        padding = full_width_space * 2 * depth
        return f"""{padding}N("{self.surface}", "{self.base}"{self.str_children(depth)})"""

    def str_children(self, depth: int) -> str:
        if not self.children: return ""

        separator = f", {newline}"
        return f""", \n{separator.join([m.repr_(depth + 1) for m in self.children])}"""

class SentenceBreakdownViewModelSpec:
    def __init__(self, *nodes: NodeViewModelSpec):
        self.nodes = list(nodes)

    def __repr__(self) -> str:
        separator = ", \n"
        return f"""S(
{separator.join([m.repr_(1) for m in self.nodes])})"""

    def repr_single_line(self) -> str:
        return "".join(repr(self).split("\n")).replace(full_width_space, "")

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, SentenceBreakdownViewModelSpec)
                and other.nodes == self.nodes)

    @staticmethod
    def from_view_model(model: BreakDownViewModel) -> SentenceBreakdownViewModelSpec:
        return SentenceBreakdownViewModelSpec(*[NodeViewModelSpec.from_view_model(view_model) for view_model in model.nodes])
