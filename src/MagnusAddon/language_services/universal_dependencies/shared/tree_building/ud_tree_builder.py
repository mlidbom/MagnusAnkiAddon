from __future__ import annotations

from typing import Callable, TypeAlias

from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building.compound_builder_base import CompoundBuilderBase
from language_services.universal_dependencies.shared.tree_building.rules_based_compound_builder import RulesBasedCompoundBuilder
from language_services.universal_dependencies.shared.tree_building.ud_tree import UDTree
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode

BuilderFactory: TypeAlias = Callable[[list[UDToken], int], CompoundBuilderBase]

class _Depth:
    surface_0 = 0
    depth_1 = 1
    depth_2 = 2
    depth_3 = 3
    morphemes_10 = 10

def build_tree(parser: UDTokenizer, text: str, builder_factory: BuilderFactory | None = None) -> UDTree:
    if not builder_factory:
        def rules_based_compound_builder_factory(unconsumed_tokens: list[UDToken], _depth: int) -> CompoundBuilderBase:
            return RulesBasedCompoundBuilder(unconsumed_tokens, _depth)
        builder_factory = rules_based_compound_builder_factory

    tokens = parser.tokenize(text).tokens
    depth = 0
    compounds = _build_compounds(tokens, depth, builder_factory)
    return UDTree(*[_create_node(compound, depth, builder_factory) for compound in compounds])

def _build_compounds(tokens: list[UDToken], depth: int, builder_factory: Callable[[list[UDToken], int], CompoundBuilderBase]) -> list[list[UDToken]]:
    created_compounds: list[list[UDToken]] = []
    unconsumed_tokens = tokens.copy()

    while unconsumed_tokens:
        created_compounds.append(builder_factory(unconsumed_tokens, depth).build())

    return created_compounds

def _create_node(tokens: list[UDToken], depth: int, builder_factory: BuilderFactory) -> 'UDTreeNode':
    children = [] if len(tokens) == 1 else _build_child_compounds(tokens, depth + 1, builder_factory)

    return UDTreeNode(depth, children, tokens)

def _build_child_compounds(parent_node_tokens: list[UDToken], depth: int, builder_factory: BuilderFactory) -> list[UDTreeNode]:
    if len(parent_node_tokens) == 1:
        return []

    compounds = _build_compounds(parent_node_tokens, depth, builder_factory)

    while len(compounds) == 1:  # if len == 1 the result is identical to the parent, go down in granularity and try again
        depth += 1
        compounds = _build_compounds(parent_node_tokens, depth, builder_factory)

    return [_create_node(phrase, depth, builder_factory) for phrase in compounds]
