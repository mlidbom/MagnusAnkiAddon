from __future__ import annotations

from language_services.universal_dependencies.shared.tokenizing import deprel, xpos
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tree_building.compound_builder_base import CompoundBuilderBase, CompoundingRuleSet
from language_services.universal_dependencies.shared.tree_building.compound_predicates import CompoundPredicates

class BottomUpdCompoundBuilder(CompoundBuilderBase):
    def __init__(self, source_token: list[UDToken], depth: int):
        super().__init__(source_token, depth)
        predicates = CompoundPredicates(self)

        self.depth_rules: list[CompoundingRuleSet] = [
            CompoundingRuleSet(
                join_when=[
                    predicates.next_is_dependent_of_compound(),
                    predicates.compound_is_missing_head(deprel.compound),
                    predicates.next_is_head_of_current(deprel.compound,
                                                       deprel.nominal_subject,
                                                       deprel.oblique_nominal,
                                                       deprel.clausal_modifier_of_noun),
                    #predicates.next_is_head_of_compound_token(deprel.nominal_subject),
                ],
                split_when=[
                    # predicates.next_has_xpos(xpos.particle_phrase_ending),
                    # predicates.next_has_deprel(deprel.case_marking)
                ]
            ),
            # CompoundingRuleSet(
            #     join_when=[predicates.true],
            #     split_when=[
            #         predicates.next_is_first_token_with_xpos(xpos.inflecting_dependent_word),
            #         predicates.next_is_first(deprel.marker),
            #         predicates.next_is_first(deprel.case_marking),
            #     ]),
            #
            # CompoundingRuleSet(join_when=[
            #     predicates.next_shares_head_with_current()
            # ]),
            # CompoundingRuleSet(join_when=[
            #     predicates.next_shares_head_and_deprel_with_current(deprel.case_marking)
            # ]),

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

    @staticmethod
    def create(source_token: list[UDToken], depth: int) -> BottomUpdCompoundBuilder:
        return BottomUpdCompoundBuilder(source_token, depth)
