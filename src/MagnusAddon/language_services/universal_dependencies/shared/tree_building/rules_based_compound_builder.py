from __future__ import annotations

from language_services.universal_dependencies.shared.tokenizing import deprel, xpos
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tree_building.compound_builder_base import CompoundBuilderBase, CompoundingRuleSet
from language_services.universal_dependencies.shared.tree_building.compound_predicates import CompoundPredicates

class RulesBasedCompoundBuilder(CompoundBuilderBase):
    def __init__(self, source_token: list[UDToken], depth: int):
        super().__init__(source_token, depth)
        predicates = CompoundPredicates(self)

        self.depth_rules: list[CompoundingRuleSet] = [
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_dependent_of_compound(),

                    predicates.next_is_head_of_current(deprel.compound),
                    predicates.current_is_nominal_subject_or_oblique_nominal_of_next_that_is_adjective_i_bound,

                    predicates.next_shares_head_with_current_and_head_is_in_compound,
                    predicates.next_shares_head_and_xpos_with_current(xpos.particle_phrase_ending)
                ],
                split_when=[
                    predicates.next_is_first_token_with_xpos(xpos.particle_phrase_ending)
                ]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_dependent_of_compound(deprel.fixed_multiword_expression),
                    predicates.next_is_dependent_of_current(deprel.compound),

                    predicates.next_shares_head_with_current_and_head_is_past_token,
                    predicates.next_is_head_of_current()
                ],
                split_when=[
                    predicates.next_is_head_of_current(deprel.numeric_modifier)
                ]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_dependent_of_compound(deprel.fixed_multiword_expression),
                    predicates.next_is_dependent_of_current(deprel.compound),
                ],
                split_when=[
                ]
            ),
            # below here is just there to make debugging and understanding easier.
            # When the level is around 10 we know that none of our rules are in play anymore.
            CompoundingRuleSet(join_when=[predicates.true], split_when=[]),
            CompoundingRuleSet(join_when=[predicates.true], split_when=[]),
            CompoundingRuleSet(join_when=[predicates.true], split_when=[]),
            CompoundingRuleSet(join_when=[predicates.true], split_when=[]),
            CompoundingRuleSet(join_when=[predicates.true], split_when=[]),
            CompoundingRuleSet(join_when=[predicates.true], split_when=[]),
            CompoundingRuleSet(join_when=[predicates.true], split_when=[])
        ]
