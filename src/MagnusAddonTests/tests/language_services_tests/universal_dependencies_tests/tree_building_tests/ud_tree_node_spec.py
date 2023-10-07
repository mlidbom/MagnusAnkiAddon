from __future__ import annotations

from typing import Any

from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests import ud_tree_node_spec_formatter

class UDTreeNodeSpec:
    def __init__(self, surface: str, lemma: str, children: list[UDTreeNodeSpec] | None = None) -> None:
        self.surface = surface
        self.lemma = lemma if lemma else surface
        self.children = children if children else []
        self.token: UDToken | None = None


    def __str__(self) -> str: return ud_tree_node_spec_formatter.str_(self, 0)
    def __repr__(self) -> str: return ud_tree_node_spec_formatter.repr_(self, 0)

    def __eq__(self, other:Any) -> bool:
        return (isinstance(other, UDTreeNodeSpec)
                and other.surface == self.surface
                and other.lemma == self.lemma
                and other .children == self.children)

    @classmethod
    def from_node(cls, node:UDTreeNode) -> UDTreeNodeSpec:
        spec = UDTreeNodeSpec(node.surface, node.lemma, [cls.from_node(child) for child in node.children])
        if node.is_morpheme():
            spec.token = node.tokens[0]

        return spec
