from __future__ import annotations
from typing import TYPE_CHECKING

from sysutils.ex_str import full_width_space

if TYPE_CHECKING:
    from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode

from sysutils import kana_utils
from sysutils import ex_str


def _str_pos(node: UDTreeNode) -> str:
    if node.is_morpheme():
        token = node.tokens[0]
        return (f"""{ex_str.pad_to_length(str(token.id), 3)}""" +
                f"""{ex_str.pad_to_length(str(token.head.id), 3)}""" +
                f"""{ex_str.pad_to_length(token.deprel.description, 28)}""" +
                f"""{ex_str.pad_to_length(token.xpos.description, 30)}""" +
                f"""{ex_str.pad_to_length(token.upos.description, 26)}""" +
                f"""feat:{token.feats} deps:{token.deps} misc:{token.misc}""")
    return "_"


def _indent(level: int) -> str: return full_width_space * 2 * level

def _children_str(node: UDTreeNode, level:int = 1) -> str:
    if not node.children:
        return ""

    line_start = f'\n'
    children_string = line_start.join(str_(child, level) for child in node.children)
    return f"""{line_start}{children_string}"""


def str_(node: UDTreeNode, level: int) -> str:
    indent = full_width_space * 2 * level
    start = f"""{ex_str.pad_to_length(str(node.depth), 3)}{indent}{node.form}{f"{full_width_space}－{full_width_space}" + node.lemma if node.lemma_differs_from_form() else ""}"""
    start = kana_utils.pad_to_length(start, 20)
    return f"""{start}{_str_pos(node)}{_children_str(node, level + 1)}"""