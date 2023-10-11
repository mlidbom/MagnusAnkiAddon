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

                    predicates.next_is_head_of_current(deprel.compound, deprel.nominal_subject, deprel.oblique_nominal),
                    predicates.next_is_head_of_compound_token(deprel.nominal_subject),

                    # keeps the particle_phrase_ending we split off below together in one compound.
                    predicates.next_shares_head_and_xpos_with_current(xpos.particle_phrase_ending),
                    #predicates.next_shares_head_with_current_and_current_is_deprel(deprel.copula)
                ],
                split_when=[
                    predicates.next_is_first_token_with_xpos(xpos.particle_phrase_ending),
                    #predicates.next_is_dependent_of_current(deprel.copula)
                ]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_shares_head_with_current_and_head_is_past_token,
                    predicates.next_is_head_of_compound_token(deprel.nominal_subject),
                    predicates.next_is_dependent_of_compound(deprel.fixed_multiword_expression),
                    predicates.next_is_dependent_of_current(deprel.compound, deprel.case_marking),
                    predicates.next_is_head_of_current(deprel.compound),
                ],
                split_when=[predicates.next_is_first_token_with_xpos(xpos.particle_conjunctive)]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_dependent_of_compound(deprel.fixed_multiword_expression,
                                                             deprel.compound),
                    predicates.next_is_head_of_compound_token(deprel.compound),
                    predicates.next_shares_head_with_current(deprel.case_marking)
                ],
                split_when=[predicates.current_is_particle_conjunctive_and_next_is_verb_bound]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_dependent_of_compound(deprel.fixed_multiword_expression),
                    predicates.next_is_dependent_of_current(deprel.compound),
                ]
            ),
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_dependent_of_current(deprel.compound)
                ]
            ),

            # below here is just there to make debugging and understanding easier.
            # When the level is around 10 we know that none of our rules are in play anymore.
            CompoundingRuleSet(join_when=[predicates.true]),
            CompoundingRuleSet(join_when=[predicates.true]),
            CompoundingRuleSet(join_when=[predicates.true]),
            CompoundingRuleSet(join_when=[predicates.true]),
            CompoundingRuleSet(join_when=[predicates.true]),

            # if nothing else matches, just split into individual tokens.
            # I sort of feel we should never reach here, but we sure do at the moment.
            CompoundingRuleSet(join_when=[], split_when=[predicates.true])
        ]
