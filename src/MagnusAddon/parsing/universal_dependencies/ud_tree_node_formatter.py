from __future__ import annotations
from typing import TYPE_CHECKING

from sysutils.ex_str import full_width_space

if TYPE_CHECKING:
    from parsing.universal_dependencies.ud_tree_node import UDTextTreeNode

from sysutils import kana_utils
from sysutils import ex_str


def _str_pos(self: UDTextTreeNode) -> str:
    if self.is_morpheme():
        token = self.tokens[0]
        return (f"""{ex_str.pad_to_length(str(token.id), 3)}""" +
                f"""{ex_str.pad_to_length(str(token.head.id), 3)}""" +
                f"""{ex_str.pad_to_length(token.deprel.description, 28)}""" +
                f"""{ex_str.pad_to_length(token.xpos.description, 30)}""" +
                f"""{ex_str.pad_to_length(token.upos.description, 26)}""" +
                f"""feat:{token.feats} deps:{token.deps} misc:{token.misc}""")
    return "_"


def _children_repr(self: UDTextTreeNode, level:int = 1) -> str:
    if not self.children:
        return ""
    children_string = ', \n'.join(repr_(child, level) for child in self.children)
    return f""", [\n{children_string}]"""

def _indent(level: int) -> str: return full_width_space * 2 * level

def repr_(self: UDTextTreeNode, level: int) -> str:
    return f"""{_indent(level)}N('{self.surface}', '{self.base if self.base_differs_from_surface() else ""}'{_children_repr(self, level + 1)})"""


def _children_str(self: UDTextTreeNode, level:int = 1) -> str:
    if not self.children:
        return ""

    line_start = f'\n'
    children_string = line_start.join(str_(child, level) for child in self.children)
    return f"""{line_start}{children_string}"""


def str_(self: UDTextTreeNode, level: int) -> str:
    indent = full_width_space * 2 * level
    start = f"""{indent}{self.surface}{f"{full_width_space}－{full_width_space}" + self.base if self.base_differs_from_surface() else ""}"""
    start = kana_utils.pad_to_length(start, 20)
    return f"""{start}{_str_pos(self)}{_children_str(self, level + 1)}"""