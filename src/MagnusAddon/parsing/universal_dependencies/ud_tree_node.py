from typing import Callable

from parsing.universal_dependencies import ud_tree_parser
from parsing.universal_dependencies.core.ud_token import UDToken
from sysutils import kana_utils
from sysutils.stringutils import StringUtils


class UDTreeNode:
    _max_lookahead = 12

    def __init__(self, surface: str, base: str, children: list['UDTreeNode'] = None, tokens: list[UDToken] = None) -> None:
        self.surface = surface
        self.base = base if base else surface
        self.tokens = tokens
        self.children: list[UDTreeNode] = children if children else []

    def is_morpheme(self) -> bool:
        return not self.children

    def is_inflected(self) -> bool:
        return self.base != self.surface

    def visit(self, callback: Callable[['UDTreeNode'],None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)


    def _str_pos(self) -> str:
        if self.is_morpheme():
            token = self.tokens[0]
            return (f"""{StringUtils.pad_to_length(str(token.id), 3)}""" +
                    f"""{StringUtils.pad_to_length(str(token.head.id), 3)}""" +  # noqa
                    f"""{StringUtils.pad_to_length(token.deprel.description, 28)}""" +
                    f"""{StringUtils.pad_to_length(token.xpos.description, 30)}""" +
                    f"""{StringUtils.pad_to_length(token.upos.description, 26)}""" +
                    f"""feat:{token.feats} deps:{token.deps} misc:{token.misc}""")
        return "_"

    def _children_repr(self, level=1) -> str:
        if not self.children:
            return ""
        children_string = ', \n'.join(child._repr(level) for child in self.children)
        return f""", [\n{children_string}]"""

    def _repr(self, level: int):
        indent = "　　" * level
        return f"""{indent}N('{self.surface}', '{self.base if self.is_inflected() else ""}'{self._children_repr(level + 1)})"""

    def _children_str(self, level=1) -> str:
        if not self.children:
            return ""

        line_start = f'\n'
        children_string = line_start.join(child._str(level) for child in self.children)
        return f"""{line_start}{children_string}"""

    def _str(self, level: int):
        indent = "　　" * level
        start = f"""{indent}{self.surface}{"　－　" + self.base if self.is_inflected() else ""}"""
        start = kana_utils.pad_to_length(start, 20)
        return f"""{start}{self._str_pos()}{self._children_str(level + 1)}"""

    def __repr__(self) -> str:
        return self._repr(0)

    def __eq__(self, other: any) -> bool:
        return (isinstance(other, UDTreeNode)
                and self.base == other.base
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)
