from typing import Callable, Optional, Any

from parsing.universal_dependencies import ud_tree_node_formatter
from parsing.universal_dependencies.core.ud_token import UDToken

class UDTreeNode:
    def __init__(self, surface: str, base: str, children: Optional[list['UDTreeNode']] = None, tokens: Optional[list[UDToken]] = None) -> None:
        self.surface = surface
        self.base = base if base else surface
        self.tokens:list[UDToken] = tokens if tokens else []
        self.children: list[UDTreeNode] = children if children else []

    def is_morpheme(self) -> bool: return not self.children

    def is_inflected(self) -> bool: return self.base != self.surface

    def visit(self, callback: Callable[['UDTreeNode'],None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)

    def __str__(self) -> str: return ud_tree_node_formatter.str_(self, 0)
    def __repr__(self) -> str: return ud_tree_node_formatter.repr_(self, 0)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, UDTreeNode)
                and self.base == other.base
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int: return hash(self.surface)
