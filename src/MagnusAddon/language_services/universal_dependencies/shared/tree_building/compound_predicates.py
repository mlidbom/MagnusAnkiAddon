from __future__ import annotations

from typing import Callable

from language_services.universal_dependencies.shared.tokenizing import deprel, xpos
from language_services.universal_dependencies.shared.tokenizing.deprel import UdRelationshipTag
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tokenizing.xpos import UdJapanesePartOfSpeechTag
from language_services.universal_dependencies.shared.tree_building.compound_builder import CompoundBuilder

class CompoundPredicates:
    def __init__(self, compound: CompoundBuilder):
        self.compound = compound

    @property
    def _next(self) -> UDToken: return self.compound.next
    @property
    def _current(self) -> UDToken: return self.compound.current
    @property
    def _compound_tokens(self) -> list[UDToken]: return self.compound.compound_tokens
    @property
    def _source_tokens(self) -> list[UDToken]: return self.compound.source_tokens

    def nexts_head_is_compound_token(self) -> bool:
        return self.compound.next.head in set(self.compound.compound_tokens)

    def current_is_nominal_subject_or_oblique_nominal_of_next_that_is_adjective_i_bound(self) -> bool:
        return (self._current.deprel in {deprel.nominal_subject, deprel.oblique_nominal}
                and self._current.head == self._next
                and self._current.head.xpos in {xpos.adjective_i_bound })

    def next_is_head_of_compound_token(self) -> bool:
        return self.compound.next in set(token.head for token in self.compound.compound_tokens)

    def next_is_compound_dependent_on_current(self) -> bool:
        return self.compound.next.deprel == deprel.compound and self.compound.next.head == self.compound.current

    def true(self) -> bool: return True # noqa

    def next_is_first_xpos(self, _xpos: UdJapanesePartOfSpeechTag) -> Callable[[], bool]:
        return lambda: self.compound.next.xpos == _xpos and self.compound.current.xpos != _xpos

    def current_is_last_sequential_deprel(self, deprel_: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self.compound.current.deprel == deprel_ and self.compound.next.deprel != deprel_

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
        return self.compound.next.head.id <= self.compound.current.id and self.compound.next.deprel == deprel.fixed_multiword_expression

    def next_is_first_deprel(self, _deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self.compound.next.deprel == _deprel and self.compound.current.deprel != _deprel

    def _tokens_missing_heads(self) -> list[UDToken]:
        return [tok for tok in self.compound.compound_tokens if tok.head.id > self.compound.current.id]

    def missing_token(self, token: UDToken) -> Callable[[], bool]:
        return lambda: token not in self.compound.compound_tokens

    def next_is_child_of(self, token: UDToken) -> Callable[[], bool]:
        return lambda: self.compound.next.head == token

    def missing_deprel(self, *_deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: any(t for t in self._tokens_missing_heads() if t.deprel in _deprel)

    def missing_deprel_xpos_combo(self, *combo: tuple[UdRelationshipTag, UdJapanesePartOfSpeechTag]) -> Callable[[], bool]:
        return lambda: any(t for t in self._tokens_missing_heads() if (t.deprel, t.xpos) in combo)
