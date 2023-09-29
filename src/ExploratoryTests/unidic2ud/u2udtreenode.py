from typing import Callable

from unidic2ud import UDPipeEntry
from src.ExploratoryTests.unidic2ud import u2udtreeparser, ud_japanese_pos_tags, universal_dependency_relationships
from sysutils import kana_utils
from sysutils.stringutils import StringUtils


class U2UdTreeNode:
    _max_lookahead = 12

    def __init__(self, surface: str, base: str, children: list['U2UdTreeNode'] = None, tokens: list[UDPipeEntry] = None) -> None:
        self.surface = surface
        self.base = base if base else surface
        self.tokens = tokens
        self.children: list[U2UdTreeNode] = children if children else []

    def is_leaf_node(self) -> bool:
        return len(self.tokens) == 1

    def is_inflected(self) -> bool:
        return self.base != self.surface

    def visit(self, callback: Callable[['U2UdTreeNode'],None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)

    @classmethod
    def create(cls, tokens: list[UDPipeEntry], depth:int) -> 'U2UdTreeNode':
        if len(tokens) > 1:
            if depth > 1: # we may still get something of value from the token parsing
                children = u2udtreeparser.parse_recursive(tokens, depth - 1)
            else: # no more compounds will be found, just add the tokens as children
                children = [cls.create_simple([token], []) for token in tokens]
        else:
            children = []

        return cls.create_simple(tokens, children)

    @classmethod
    def create_simple(cls, tokens: list[UDPipeEntry], children: list['U2UdTreeNode']) -> 'U2UdTreeNode':
        surface = "".join(tok.form for tok in tokens)
        base = "".join(tok.form for tok in tokens[:-1]) + tokens[-1].lemma
        return U2UdTreeNode(surface, base, children, tokens)


    def _children_repr(self, level=1) -> str:
        if not self.children:
            return ""
        indent = "  " * level
        children_string = ', '.join(child._repr(level) for child in self.children)
        return f""",[\n{indent}{children_string}]"""

    def _children_str(self, level=1) -> str:
        if not self.children:
            return ""

        line_start = f'\n'
        children_string = line_start.join(child._str(level) for child in self.children)
        return f"""{line_start}{children_string}"""

    def _repr(self, level: int):
        return f"""N('{self.surface}', '{self.base if self.is_inflected() else ""}'{self._children_repr(level + 1)})"""



    def _str_pos(self) -> str:
        if self.is_leaf_node():
            token = self.tokens[0]
            return (f"""{StringUtils.pad_to_length(str(token.id), 3)}""" +
                    f"""{StringUtils.pad_to_length(str(token.head.id), 3)}""" + # noqa
                    f"""{StringUtils.pad_to_length(universal_dependency_relationships.get_tag(token.deprel).description, 28)}""" +
                    f"""{StringUtils.pad_to_length(ud_japanese_pos_tags.get_tag(token.xpos).english_description, 30)}""" +
                    f"""{StringUtils.pad_to_length(token.upos, 7)}""" +
                    f"""feat:{token.feats} deps:{token.deps} misc:{token.misc}""")
        return "_"

    def _str(self, level: int):
        indent = "　　" * level
        start = f"""{indent}{self.surface}{"　－　" + self.base if self.is_inflected() else ""}"""
        start = kana_utils.pad_to_length(start, 20)
        return f"""{start}{self._str_pos()}{self._children_str(level + 1)}"""

    def __repr__(self) -> str:
        return self._repr(0)

    def __eq__(self, other: any) -> bool:
        return (isinstance(other, U2UdTreeNode)
                and self.base == other.base
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)
