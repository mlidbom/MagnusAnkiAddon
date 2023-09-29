from typing import Callable

from unidic2ud import UDPipeEntry
from src.ExploratoryTests.unidic2ud import u2udtreeparser


class U2UdTreeNode:
    _max_lookahead = 12

    def __init__(self, surface: str, base: str, children: list['U2UdTreeNode'] = None, tokens: list[UDPipeEntry] = None) -> None:
        self.surface = surface
        self.base = base if base else surface
        self.tokens = tokens
        self.children: list[U2UdTreeNode] = children if children else []

    def _children_repr(self, level=1) -> str:
        if not self.children:
            return ""
        indent = "  " * level
        children_string = ', '.join(child._repr(level) for child in self.children)
        return f""",[\n{indent}{children_string}]"""

    def _repr(self, level: int):
        return f"""N('{self.surface}', '{self.base if self.is_inflected() else ""}'{self._children_repr(level + 1)})"""

    def __repr__(self) -> str:
        return self._repr(0)

    def __eq__(self, other: any) -> bool:
        return (isinstance(other, U2UdTreeNode)
                and self.base == other.base
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)

    def is_inflected(self) -> bool:
        return self.base != self.surface

    def visit(self, callback: Callable[['U2UdTreeNode'],None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)

    @classmethod
    def create(cls, tokens: list[UDPipeEntry], depth:int) -> 'U2UdTreeNode':
        if len(tokens) > 1 and depth > 1:
            children = u2udtreeparser.parse_recursive(tokens, depth - 1)
        else:
            children = []

        return cls.create_simple(tokens, children)

    @classmethod
    def create_simple(cls, tokens: list[UDPipeEntry], children: list['U2UdTreeNode']) -> 'U2UdTreeNode':
        surface = "".join(tok.form for tok in tokens)
        base = "".join(tok.form for tok in tokens[:-1]) + tokens[-1].lemma
        return U2UdTreeNode(surface, base, children, tokens)

