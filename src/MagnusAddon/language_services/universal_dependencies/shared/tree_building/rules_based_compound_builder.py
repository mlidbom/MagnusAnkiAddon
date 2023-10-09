from __future__ import annotations

from typing import Callable

from language_services.universal_dependencies.shared.tokenizing import deprel, xpos
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tree_building.compound_builder import CompoundBuilder
from language_services.universal_dependencies.shared.tree_building.compound_predicates import CompoundPredicates

class CompoundingRuleSet:
    def __init__(self, join_when: list[Callable[[], bool]], split_when: list[Callable[[], bool]]):
        self.join_rules = join_when
        self.split_rules = split_when

class RulesBasedCompoundBuilder(CompoundBuilder):
    def __init__(self, target: list[CompoundBuilder], source_token: list[UDToken], depth: int):
        super().__init__(target, source_token)
        predicates = CompoundPredicates(self)

        self.depth = depth

        self.depth_rules: list[CompoundingRuleSet] = [
            CompoundingRuleSet(
                join_when=[
                    predicates.nexts_head_is_compound_token,
                    predicates.missing_deprel(deprel.compound),
                    predicates.next_shares_earlier_head_with_current,
                    predicates.current_is_nominal_subject_or_oblique_nominal_of_next_that_is_adjective_i_bound
                ],
                split_when=[
                    predicates.next_is_first_xpos(xpos.particle_phrase_ending)
                ]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_child_of(self.first),
                    predicates.next_is_compound_dependent_on_current,
                    predicates.next_is_fixed_multiword_expression_with_compound_token,
                    predicates.next_shares_earlier_head_with_current
                ],
                split_when=[
                ]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_fixed_multiword_expression_with_compound_token,
                    predicates.next_shares_earlier_head_with_current,
                    predicates.next_is_head_of_compound_token],
                split_when=[
                ]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_compound_dependent_on_current,
                    predicates.next_is_fixed_multiword_expression_with_compound_token],
                split_when=[
                ]
            )]

    def build(self) -> None:
        if self.depth < len(self.depth_rules):
            join_when = self.depth_rules[self.depth].join_rules
            split_when = self.depth_rules[self.depth].split_rules
        else:
            join_when = []
            split_when = []

        while self.has_next:
            for rule in split_when:
                if rule():
                    return
            consumed: bool = False
            for rule in join_when:
                if rule():
                    self.consume_next()
                    consumed = True
                    break
            if not consumed:
                return
