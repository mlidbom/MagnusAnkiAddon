from __future__ import annotations

from typing import Any

from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers import ud_tree_node_spec_formatter

class UDTreeNodeSpec:
    def __init__(self, surface: str, lemma: str, norm: str, children: list[UDTreeNodeSpec] | None = None, depth:int = -1) -> None:
        self.surface = surface
        self.lemma = lemma if lemma else surface
        self.children = children if children else []
        self.token: UDToken | None = None
        self.norm = norm
        self.depth = depth
        if self.depth == -1:
            self._set_depth(0)

    def _set_depth(self, depth: int) -> None:
        self.depth = depth
        for child in self.children:
            child._set_depth(depth + 1)


    def __str__(self) -> str: return ud_tree_node_spec_formatter.str_(self, 0)
    def __repr__(self) -> str: return ud_tree_node_spec_formatter.repr_(self, 0)

    def __eq__(self, other:Any) -> bool:
        return (isinstance(other, UDTreeNodeSpec)
                and other.surface == self.surface
                and other.lemma == self.lemma
                and other.children == self.children
                and other.norm == self.norm)

    @classmethod
    def from_node(cls, node:UDTreeNode, max_depth:int) -> UDTreeNodeSpec:
        return cls._from_node(node, 0, max_depth)

    @classmethod
    def _from_node(cls, node:UDTreeNode, depth:int, max_depth:int) -> UDTreeNodeSpec:
        spec = UDTreeNodeSpec(node.form,
                              node.lemma if node.lemma != node.form else "",
                              node.norm if node.norm != node.lemma else "",
                              [cls._from_node(child, depth, max_depth) for child in node.children if child.depth <= max_depth],
                              node.depth)
        if node.is_morpheme():
            spec.token = node.tokens[0]

        return spec