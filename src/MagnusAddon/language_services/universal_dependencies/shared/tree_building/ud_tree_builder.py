from __future__ import annotations

from typing import Callable

import sysutils.functional.predicate
from language_services.universal_dependencies.shared.tokenizing import ud_japanese_part_of_speech_tag, ud_deprel
from language_services.universal_dependencies.shared.tokenizing.ud_deprel import UdRelationshipTag
from language_services.universal_dependencies.shared.tokenizing.ud_japanese_part_of_speech_tag import UdJapanesePartOfSpeechTag
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
    morphemes_10 = 10

def build_tree(parser: UDTokenizer, text: str, collapse_identical_levels_above_level: int = -1) -> UDTree:
    tokens = parser.parse(text).tokens
    depth = 0
    compounds = _build_compounds(tokens, depth)
    if collapse_identical_levels_above_level < depth:
        while len(compounds) == 1 and depth < _Depth.depth_2:  # making the whole text into a compound is not usually desired, but above depth 2 we loose words, so don't go that deep.
            depth += 1
            compounds = _build_compounds(tokens, depth)
    return UDTree(*[_create_node(compound, depth, collapse_identical_levels_above_level) for compound in compounds])

class CompoundPredicates:
    def __init__(self, compound: CompoundBuilder):
        self.compound = compound

    def nexts_head_is_compound_token(self) -> bool:
        return self.compound.next.head in set(self.compound.compound_tokens)

    def next_is_head_of_compound_token(self) -> bool:
        return self.compound.next in set(token.head for token in self.compound.compound_tokens)

    def next_is_compound_dependent_on_current(self) -> bool:
        return self.compound.next.deprel == ud_deprel.compound and self.compound.next.head == self.compound.current

    # noinspection PyMethodMayBeStatic
    def true(self) -> bool: return True

    def next_is_first_xpos(self, xpos: UdJapanesePartOfSpeechTag) -> Callable[[], bool]:
        return lambda: self.compound.next.xpos == xpos and self.compound.current.xpos != xpos

    def current_is_last_sequential_deprel(self, deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self.compound.current.deprel == deprel and self.compound.next.deprel != deprel

    def current_is_last_sequential_deprel_xpos(self, combo: tuple[UdRelationshipTag, UdJapanesePartOfSpeechTag]) -> Callable[[], bool]:
        return lambda: ((self.compound.current.deprel, self.compound.current.xpos) == combo
                        and (self.compound.next.deprel, self.compound.next.xpos) != combo)

    def next_shares_earlier_head_with_current(self) -> bool:
        return (self.compound.current.head == self.compound.next.head
                and self.compound.current.head.id <= self.compound.current.id)

    def next_shares_head_with_current(self) -> bool:
        return self.compound.current.head == self.compound.next.head

    def next_is_currents_head(self) -> bool:
        return self.compound.next == self.compound.current.head

    def next_is_fixed_multiword_expression_with_compound_token(self) -> bool:
        return self.compound.next.head.id <= self.compound.current.id and self.compound.next.deprel == ud_deprel.fixed_multiword_expression

    def next_is_first_deprel(self, deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self.compound.next.deprel == deprel and self.compound.current.deprel != deprel

    def _tokens_missing_heads(self) -> list[UDToken]:
        return [tok for tok in self.compound.compound_tokens if tok.head.id > self.compound.current.id]

    def missing_token(self, token: UDToken) -> Callable[[], bool]:
        return lambda: token not in self.compound.compound_tokens

    def next_is_child_of(self, token: UDToken) -> Callable[[], bool]:
        return lambda: self.compound.next.head == token

    def missing_deprel(self, *deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: any(t for t in self._tokens_missing_heads() if t.deprel in deprel)

    def missing_deprel_xpos_combo(self, *combo: tuple[UdRelationshipTag, UdJapanesePartOfSpeechTag]) -> Callable[[], bool]:
        return lambda: any(t for t in self._tokens_missing_heads() if (t.deprel, t.xpos) in combo)

class CompoundBuilder:
    def __init__(self, target: list[CompoundBuilder], source_tokens: list[UDToken]):
        target.append(self)
        self.source_tokens = source_tokens
        self.compound_tokens = [source_tokens.pop(0)]
        self.stop_rules: list[Callable[[], bool]] = []
        self.go_rules: list[Callable[[], bool]] = []

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

    def consume_while(self, predicate: Predicate[UDToken]) -> None:
        self.compound_tokens += ex_list.consume_while(predicate, self.source_tokens)

    def tokens_where(self, predicate: Predicate[UDToken]) -> list[UDToken]:
        return ex_list.where(predicate, self.compound_tokens)

    def consume_rule_based(self) -> None:
        while self.has_next:
            for rule in self.stop_rules:
                if rule():
                    return
            consumed: bool = False
            for rule in self.go_rules:
                if rule():
                    self.consume_next()
                    consumed = True
                    break
            if not consumed:
                return

class RulesBasedCompoundBuilder(CompoundBuilder):
    def __init__(self, target: list[CompoundBuilder], source_token: list[UDToken], depth: int):
        super().__init__(target, source_token)
        predicates = CompoundPredicates(self)

        if depth == 0:
            self.go_rules = [
                predicates.nexts_head_is_compound_token,
                predicates.missing_deprel(ud_deprel.compound),
                predicates.next_shares_earlier_head_with_current,
                #predicates.next_shares_head_with_current
            ]
            self.stop_rules = [predicates.next_is_first_xpos(ud_japanese_part_of_speech_tag.particle_phrase_final)]
        elif depth == 1:
            self.go_rules = [predicates.next_is_child_of(self.first),
                             predicates.next_is_compound_dependent_on_current,
                             predicates.next_is_fixed_multiword_expression_with_compound_token,
                             predicates.next_shares_earlier_head_with_current,
                             ]
            self.stop_rules = []
        elif depth == 2:
            self.go_rules = [predicates.true]
            self.stop_rules = []
        elif depth == 3:
            self.go_rules = [predicates.next_is_fixed_multiword_expression_with_compound_token,
                             predicates.next_shares_earlier_head_with_current,
                             predicates.next_is_head_of_compound_token]
            self.stop_rules = []
        elif depth == 4:
            self.go_rules = [predicates.next_is_compound_dependent_on_current,
                             predicates.next_is_fixed_multiword_expression_with_compound_token]
            self.stop_rules = []
        elif depth == 5:
            self.go_rules = []
            self.stop_rules = []
        elif depth == 6:
            self.go_rules = []
            self.stop_rules = []
        elif depth == 7:
            self.go_rules = []
            self.stop_rules = []
        elif depth == 8:
            self.go_rules = []
            self.stop_rules = []
        elif depth == 9:
            self.go_rules = []
            self.stop_rules = []

        # predicates.next_is_first_phrase_end_particle,
        # predicates.current_is_last_sequential_deprel(ud_deprel.case_marking),
        # predicates.current_is_last_sequential_deprel_xpos((ud_deprel.marker, ud_japanese_part_of_speech_tag.particle_conjunctive))

def _build_compounds(tokens: list[UDToken], depth: int) -> list[list[UDToken]]:
    assert depth <= _Depth.morphemes_10
    if depth == _Depth.morphemes_10:
        return [[token] for token in tokens]

    created_compounds: list[CompoundBuilder] = []
    unconsumed_tokens = tokens.copy()

    while unconsumed_tokens:
        RulesBasedCompoundBuilder(created_compounds, unconsumed_tokens, depth).consume_rule_based()

    return [cb.compound_tokens for cb in created_compounds]

def _create_node(tokens: list[UDToken], depth: int, collapse_identical_levels_above_level: int) -> 'UDTreeNode':
    children = [] if collapse_identical_levels_above_level < depth and len(tokens) == 1 \
        else _build_child_compounds(tokens, depth + 1, collapse_identical_levels_above_level)

    return UDTreeNode(depth, children, tokens)

def _build_child_compounds(parent_node_tokens: list[UDToken], depth: int, collapse_identical_levels_above_level: int) -> list[UDTreeNode]:
    if (depth > _Depth.morphemes_10
            or depth > collapse_identical_levels_above_level and len(parent_node_tokens) == 1):
        return []

    compounds = _build_compounds(parent_node_tokens, depth)
    if collapse_identical_levels_above_level < depth:
        while len(compounds) == 1 and depth <= _Depth.morphemes_10:  # if len == 1 the result is identical to the parent, go down in granularity and try again
            depth += 1
            compounds = _build_compounds(parent_node_tokens, depth)

    return [_create_node(phrase, depth, collapse_identical_levels_above_level) for phrase in compounds]
