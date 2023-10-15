from __future__ import annotations
from typing import TYPE_CHECKING

from sysutils.ex_str import full_width_space

if TYPE_CHECKING:
    from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_node_spec import UDTreeNodeSpec

from sysutils import kana_utils
from sysutils import ex_str


def _str_pos(node: UDTreeNodeSpec) -> str:
    if not node.children and node.token:
        token = node.token
        return (f"""{ex_str.pad_to_length(str(token.id), 3)}""" +
                f"""{ex_str.pad_to_length(str(token.head.id), 3)}""" +
                f"""{ex_str.pad_to_length(token.deprel.description, 28)}""" +
                f"""{ex_str.pad_to_length(token.xpos.description, 30)}""" +
                f"""{ex_str.pad_to_length(token.upos.description, 26)}""" #+
                # f"""feat:{token.feats}""" +
                # f""" deps:{token.deps} misc:{token.misc}""" +
                # f""" misc:{token.misc}"""
                )
    return "_"


def _children_repr(node: UDTreeNodeSpec, level:int = 1) -> str:
    if not node.children:
        return ""
    children_string = ', \n'.join(repr_(child, level) for child in node.children)
    return f""", [\n{children_string}]"""

def _indent(level: int) -> str: return full_width_space * 2 * level

def repr_(node: UDTreeNodeSpec, level: int) -> str:
    return f"""{_indent(level)}N('{node.surface}', '{node.lemma if node.surface != node.lemma else ""}', '{node.norm}'{_children_repr(node, level + 1)})"""


def _children_str(node: UDTreeNodeSpec, level:int = 1) -> str:
    if not node.children:
        return ""

    line_start = f'\n'
    children_string = line_start.join(str_(child, level) for child in node.children)
    return f"""{line_start}{children_string}"""


def str_(node: UDTreeNodeSpec, level: int) -> str:
    start_padding = 20
    indent = full_width_space * 2 * level
    depth = ex_str.pad_to_length(str(node.depth), 3)

    lemma = f" ({node.lemma})" if node.surface != node.lemma else ""
    norm = f" [{node.norm}]" if node.norm else ""

    start = f"""{indent}{node.surface}{lemma}{norm}"""

    if lemma: start_padding += 1
    if norm: start_padding += 1

    start = kana_utils.pad_to_length(start, start_padding)

    return f"""{depth}{start}{_str_pos(node)}{_children_str(node, level + 1)}"""