from __future__ import annotations
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode
from language_services.universal_dependencies.shared.tree_building.ud_tree import UDTree
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from sysutils import ex_list, ex_predicate

class _Depth:
    surface_0 = 0
    depth_1 = 1
    depth_2 = 2
    depth_3 = 3
    morphemes_4 = 4

def build_tree(parser: UDTokenizer, text: str) -> UDTree:
    tokens = parser.parse(text).tokens
    depth = 0
    compounds = _build_compounds(tokens, depth)
    while len(compounds) == 1 and depth < _Depth.depth_2:  # making the whole text into a compound is not usually desired, but above depth 2 we loose words, so don't go that deep.
        depth += 1
        compounds = _build_compounds(tokens, depth)
    return UDTree(*[_create_node(compound, depth) for compound in compounds])

class CompoundBuilder:
    def __init__(self, source_token: list[UDToken], compound_tokens: list[UDToken]):
        self.source_tokens = source_token
        self.compound_tokens = compound_tokens

    @property
    def next(self) -> UDToken: return self.source_tokens[0]
    @property
    def first(self) -> UDToken: return self.compound_tokens[0]
    @property
    def has_next(self) -> bool: return len(self.source_tokens) > 0

    def consume_next(self) -> None:
        self.compound_tokens.append(self.source_tokens.pop(0))

    def consume_while_child_of_first(self) -> None:
        self.compound_tokens += ex_list.consume_while(self.first.is_head_of, self.source_tokens)

    def consume_while_child_of(self, token: UDToken) -> None:
        self.compound_tokens += ex_list.consume_while(token.is_head_of, self.source_tokens)

    def consume_while_child_of_next(self) -> None:
        self.consume_while_child_of(self.next)

    def consume_until_and_including(self, token: UDToken) -> None:
        self.compound_tokens += ex_list.consume_until_and_including(ex_predicate.eq_(token), self.source_tokens)

    @staticmethod
    def start_compound_by_consuming_first_from(source_tokens: list[UDToken]) -> CompoundBuilder:
        compound_tokens = [source_tokens.pop(0)]
        return CompoundBuilder(source_tokens, compound_tokens)

def _build_compounds(tokens: list[UDToken], depth: int) -> list[list[UDToken]]:
    assert depth <= _Depth.morphemes_4
    if depth == _Depth.morphemes_4:
        return [[token] for token in tokens]

    created_compounds: list[CompoundBuilder] = []
    unconsumed_tokens = tokens.copy()

    while unconsumed_tokens:
        compound = CompoundBuilder.start_compound_by_consuming_first_from(unconsumed_tokens)
        created_compounds.append(compound)

        if depth == _Depth.depth_3:
            compound.consume_while_child_of(compound.first)

        elif depth == _Depth.depth_2:
            compound.consume_while_child_of(compound.first)
            if compound.first.head.id == compound.first.id + 1:  # head of first is second token
                compound.consume_next()
                compound.consume_while_child_of(compound.first.head)

        elif depth == _Depth.depth_1:
            compound.consume_while_child_of(compound.first)
            if compound.has_next and compound.next == compound.first.head:
                compound.consume_next()
                compound.consume_while_child_of(compound.first.head)

        elif depth == _Depth.surface_0:
            compound.consume_while_child_of(compound.first)
            compound.consume_until_and_including(compound.first.head)
            compound.consume_while_child_of(compound.first.head)

    return [cb.compound_tokens for cb in created_compounds]

def _create_node(tokens: list[UDToken], depth: int) -> 'UDTreeNode':
    children = _build_child_compounds(tokens, depth + 1) if len(tokens) > 1 else []
    surface = "".join(tok.form for tok in tokens)
    base = "".join(tok.form for tok in tokens[:-1]) + tokens[-1].lemma
    return UDTreeNode(surface, base, children, tokens)

def _build_child_compounds(parent_node_tokens: list[UDToken], depth: int) -> list[UDTreeNode]:
    compounds = _build_compounds(parent_node_tokens, depth)
    while len(compounds) == 1 and depth <= _Depth.morphemes_4:  # if len == 1 the result is identical to the parent, go down in granularity and try again
        depth += 1
        compounds = _build_compounds(parent_node_tokens, depth)

    return [_create_node(phrase, depth) for phrase in compounds]
