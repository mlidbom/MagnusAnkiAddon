from typing import Callable

from unidic2ud import UDPipeEntry

from parsing.universal_dependencies import ud2ud_tree_parser, ud_relationship_tag, ud_japanese_part_of_speech_tag
from sysutils import kana_utils
from sysutils.stringutils import StringUtils


class UD2UDTreeNode:
    _max_lookahead = 12

    def __init__(self, surface: str, base: str, children: list['UD2UDTreeNode'] = None, tokens: list[UDPipeEntry] = None) -> None:
        self.surface = surface
        self.base = base if base else surface
        self.tokens = tokens
        self.children: list[UD2UDTreeNode] = children if children else []

    def is_morpheme(self) -> bool:
        return not self.children

    def is_inflected(self) -> bool:
        return self.base != self.surface

    def visit(self, callback: Callable[['UD2UDTreeNode'],None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)

    @classmethod
    def create(cls, tokens: list[UDPipeEntry], depth:int) -> 'UD2UDTreeNode':
        # noinspection PyProtectedMember
        children = ud2ud_tree_parser._parse_recursive(tokens, depth + 1) if len(tokens) > 1 else []
        surface = "".join(tok.form for tok in tokens)
        base = "".join(tok.form for tok in tokens[:-1]) + tokens[-1].lemma
        return UD2UDTreeNode(surface, base, children, tokens)


    def _str_pos(self) -> str:
        if self.is_morpheme():
            token = self.tokens[0]
            return (f"""{StringUtils.pad_to_length(str(token.id), 3)}""" +
                    f"""{StringUtils.pad_to_length(str(token.head.id), 3)}""" +  # noqa
                    f"""{StringUtils.pad_to_length(ud_relationship_tag.get_tag(token.deprel).description, 28)}""" +
                    f"""{StringUtils.pad_to_length(ud_japanese_part_of_speech_tag.get_tag(token.xpos).description, 30)}""" +
                    f"""{StringUtils.pad_to_length(token.upos, 7)}""" +
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
        return (isinstance(other, UD2UDTreeNode)
                and self.base == other.base
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)
