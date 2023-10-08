from __future__ import annotations

import sysutils.functional.predicate
from language_services.universal_dependencies.shared.tokenizing import ud_japanese_part_of_speech_tag, ud_deprel
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building.ud_tree import UDTree
from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode
from sysutils import ex_list
from sysutils.functional.predicate import Predicate

class _Depth:
    surface_0 = 0
    depth_1 = 1
    depth_2 = 2
    depth_3 = 3
    morphemes_4 = 4

def build_tree(parser: UDTokenizer, text: str, collapse_identical_levels_above_level: int = -1) -> UDTree:
    tokens = parser.parse(text).tokens
    depth = 0
    compounds = _build_compounds(tokens, depth)
    if collapse_identical_levels_above_level < depth:
        while len(compounds) == 1 and depth < _Depth.depth_2:  # making the whole text into a compound is not usually desired, but above depth 2 we loose words, so don't go that deep.
            depth += 1
            compounds = _build_compounds(tokens, depth)
    return UDTree(*[_create_node(compound, depth, collapse_identical_levels_above_level) for compound in compounds])

class CompoundBuilder:
    def __init__(self, target: list[CompoundBuilder], source_tokens: list[UDToken]):
        target.append(self)
        self.source_tokens = source_tokens
        self.compound_tokens = [source_tokens.pop(0)]

    @property
    def current(self) -> UDToken: return self.compound_tokens[-1]
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
        self.compound_tokens += ex_list.consume_until_and_including(sysutils.functional.predicate.eq_(token), self.source_tokens)

    def consume_all_descendents_of_current(self) -> None:
        parents: set[UDToken] = {self.current}
        while self.has_next and self.next.head in parents:
            parents.add(self.next)
            self.consume_next()

    def consume_all_allowed_descendents_of_compound_tokens(self) -> bool:
        parents: set[UDToken] = set(self.compound_tokens)
        while self.has_next and self.next.head in parents:
            if self._is_next_allowed_descendent():
                parents.add(self.next)
                self.consume_next()
            else:
                return False

        return True

    def _is_next_allowed_descendent(self) -> bool:
        return True

    def consume_while(self, predicate: Predicate[UDToken]) -> None:
        self.compound_tokens += ex_list.consume_while(predicate, self.source_tokens)

    def _tokens_where(self, predicate: Predicate[UDToken]) -> list[UDToken]:
        return ex_list.where(predicate, self.compound_tokens)

class Level0CompoundBuilder(CompoundBuilder):
    def __init__(self, target: list[CompoundBuilder], source_token: list[UDToken]):
        super().__init__(target, source_token)

    def _should_be_compounded_with_forward_root(self, token: UDToken) -> bool:
        if token.head.id <= self.current.id:
            return False

        if token.deprel in {ud_deprel.compound,
                            ud_deprel.clausal_modifier_of_noun,
                            ud_deprel.case_marking}:
            return True

        if (token.deprel, token.xpos) in {
            (ud_deprel.adverbial_clause_modifier, ud_japanese_part_of_speech_tag.adjective_i_bound),
            (ud_deprel.clausal_modifier_of_noun, ud_japanese_part_of_speech_tag.verb_bound)
        }:
            return True

        return False

    def _is_next_allowed_descendent(self) -> bool:
        return True

    def tokens_needed_to_be_compounded_with_forward_head(self) -> list[UDToken]:
        return self._tokens_where(self._should_be_compounded_with_forward_root)

    def build(self) -> None:
        self.consume_all_allowed_descendents_of_compound_tokens()
        while self.tokens_needed_to_be_compounded_with_forward_head():
            token_to_compound_head_for = self.tokens_needed_to_be_compounded_with_forward_head()[0]
            self.consume_until_and_including(token_to_compound_head_for.head)
            self.consume_all_allowed_descendents_of_compound_tokens()

class Level1SplitPhraseEndParticleCompoundBuilder(Level0CompoundBuilder):
    def __init__(self, target: list[CompoundBuilder], source_token: list[UDToken]):
        super().__init__(target, source_token)

    def _is_next_allowed_descendent(self) -> bool:
        if self.is_phrase_end_particle(self.next) and not self.is_phrase_end_particle(self.current):
            return False

        return True

    @staticmethod
    def is_phrase_end_particle(token:UDToken) -> bool:
        return token.xpos in {ud_japanese_part_of_speech_tag.particle_phrase_final}

    def build(self) -> None:
        if self.is_phrase_end_particle(self.current):
            self.consume_while(self.is_phrase_end_particle)
        else:
            super().build()


def _build_compounds(tokens: list[UDToken], depth: int) -> list[list[UDToken]]:
    assert depth <= _Depth.morphemes_4
    if depth == _Depth.morphemes_4:
        return [[token] for token in tokens]

    created_compounds: list[CompoundBuilder] = []
    unconsumed_tokens = tokens.copy()

    while unconsumed_tokens:
        if depth == _Depth.depth_3:
            compound = CompoundBuilder(created_compounds, unconsumed_tokens)
            compound.consume_while_child_of(compound.first)

        elif depth == _Depth.depth_2:
            compound = CompoundBuilder(created_compounds, unconsumed_tokens)
            compound.consume_while_child_of(compound.first)
            if compound.first.head.id == compound.first.id + 1 and compound.has_next:  # head of first is second token
                compound.consume_next()
                compound.consume_while_child_of(compound.first.head)

        elif depth == _Depth.depth_1:
            Level1SplitPhraseEndParticleCompoundBuilder(created_compounds, unconsumed_tokens).build()

        elif depth == _Depth.surface_0:
            Level0CompoundBuilder(created_compounds, unconsumed_tokens).build()

    return [cb.compound_tokens for cb in created_compounds]

def _create_node(tokens: list[UDToken], depth: int, collapse_identical_levels_above_level: int) -> 'UDTreeNode':
    children = [] if collapse_identical_levels_above_level < depth and len(tokens) == 1 \
        else _build_child_compounds(tokens, depth + 1, collapse_identical_levels_above_level)

    return UDTreeNode(depth, children, tokens)

def _build_child_compounds(parent_node_tokens: list[UDToken], depth: int, collapse_identical_levels_above_level: int) -> list[UDTreeNode]:
    if (depth > _Depth.morphemes_4
            or depth > collapse_identical_levels_above_level and len(parent_node_tokens) == 1):
        return []

    compounds = _build_compounds(parent_node_tokens, depth)
    if collapse_identical_levels_above_level < depth:
        while len(compounds) == 1 and depth <= _Depth.morphemes_4:  # if len == 1 the result is identical to the parent, go down in granularity and try again
            depth += 1
            compounds = _build_compounds(parent_node_tokens, depth)

    return [_create_node(phrase, depth, collapse_identical_levels_above_level) for phrase in compounds]
