from __future__ import annotations

from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building.rules_based_compound_builder import RulesBasedCompoundBuilder
from language_services.universal_dependencies.shared.tree_building.ud_tree import UDTree
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode

class _Depth:
    surface_0 = 0
    depth_1 = 1
    depth_2 = 2
    depth_3 = 3
    morphemes_10 = 10

def build_tree(parser: UDTokenizer, text: str) -> UDTree:
    tokens = parser.tokenize(text).tokens
    depth = 0
    compounds = _build_compounds(tokens, depth)
    return UDTree(*[_create_node(compound, depth) for compound in compounds])

def _build_compounds(tokens: list[UDToken], depth: int) -> list[list[UDToken]]:
    created_compounds: list[list[UDToken]] = []
    unconsumed_tokens = tokens.copy()

    while unconsumed_tokens:
        created_compounds.append(RulesBasedCompoundBuilder(unconsumed_tokens, depth).build())

    return created_compounds

def _create_node(tokens: list[UDToken], depth: int) -> 'UDTreeNode':
    children = [] if len(tokens) == 1 else _build_child_compounds(tokens, depth + 1)

    return UDTreeNode(depth, children, tokens)

def _build_child_compounds(parent_node_tokens: list[UDToken], depth: int) -> list[UDTreeNode]:
    if len(parent_node_tokens) == 1:
        return []

    compounds = _build_compounds(parent_node_tokens, depth)

    while len(compounds) == 1:  # if len == 1 the result is identical to the parent, go down in granularity and try again
        depth += 1
        compounds = _build_compounds(parent_node_tokens, depth)

    return [_create_node(phrase, depth) for phrase in compounds]
