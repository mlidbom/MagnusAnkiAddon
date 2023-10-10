from __future__ import annotations

from typing import Callable

from language_services.universal_dependencies.shared.tokenizing import deprel
from language_services.universal_dependencies.shared.tokenizing.deprel import UdRelationshipTag
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tokenizing.xpos import UdJapanesePartOfSpeechTag
from language_services.universal_dependencies.shared.tree_building.compound_predicates_base import CompoundPredicatesBase

class CompoundPredicates(CompoundPredicatesBase):
    def true(self) -> bool: return True  # noqa

    def compound_is_missing_token(self, token: UDToken) -> Callable[[], bool]:
        return lambda: token not in self.compound.tokens

    def compound_is_missing_dependent(self, *_deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: any(t for t in self._source_tokens if t.head in self._tokens or not _deprel)

    def compound_is_missing_head(self, *_deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: any(t for t in self._tokens_missing_heads() if not _deprel or t.deprel in _deprel)

    def compound_is_missing_head_with_deprel_xpos_combo(self, *combo: tuple[UdRelationshipTag, UdJapanesePartOfSpeechTag]) -> Callable[[], bool]:
        return lambda: any(t for t in self._tokens_missing_heads() if (t.deprel, t.xpos) in combo)

    def current_is_nominal_subject_or_oblique_nominal_of_next_that_is_adjective_i_bound(self) -> bool:
        return (self._current.deprel in {deprel.nominal_subject, deprel.oblique_nominal}
                and self._current.head == self._next
                #and self._current.head.xpos in {xpos.adjective_i_bound}
                )

    def current_is_last_sequential_deprel(self, deprel_: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self.compound.current.deprel == deprel_ and self.compound.next.deprel != deprel_

    def current_is_last_sequential_deprel_xpos(self, combo: tuple[UdRelationshipTag, UdJapanesePartOfSpeechTag]) -> Callable[[], bool]:
        return lambda: ((self.compound.current.deprel, self.compound.current.xpos) == combo
                        and (self.compound.next.deprel, self.compound.next.xpos) != combo)

    def next_is_dependent_of_compound(self, *_deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self._next.head in self.compound.tokens and (not _deprel or self._next.deprel in _deprel)

    def next_is_dependent_on(self, token: UDToken, *_deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self.compound.next.head == token and (not _deprel or self._next.deprel in _deprel)

    def next_is_head_of_compound_token(self, *_deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self._next in set(token.head for token in self.compound.tokens) and (not _deprel or self._next.deprel in _deprel)

    def next_is_dependent_of_current(self, *_deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self.compound.next.head == self.compound.current and self.compound.next.deprel in _deprel

    def next_is_first_token_with_xpos(self, _xpos: UdJapanesePartOfSpeechTag) -> Callable[[], bool]:
        return lambda: self.compound.next.xpos == _xpos and self.compound.current.xpos != _xpos

    def next_shares_head_with_current_and_head_is_past_token(self) -> bool:
        return (self.compound.current.head == self.compound.next.head
                and self.compound.current.head.id <= self.compound.current.id)

    def next_shares_head_with_current_and_head_is_in_compound(self) -> bool:
        return (self.compound.current.head == self.compound.next.head
                and self.compound.current.head in self.compound.tokens)

    def next_shares_head_with_current(self) -> bool:
        return self.compound.current.head == self.compound.next.head

    def next_is_first_deprel(self, _deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self.compound.next.deprel == _deprel and self.compound.current.deprel != _deprel

    def next_is_head_of_current(self, *_deprel: UdRelationshipTag) -> Callable[[], bool]:
        return lambda: self._current.head == self._next and (not _deprel or self._current.deprel in _deprel)

    def next_shares_head_and_xpos_with_current(self, _xpos: UdJapanesePartOfSpeechTag) -> Callable[[], bool]:
        return lambda: self._current.head == self._next.head and self._current.xpos == _xpos and self._next.xpos == _xpos

    def _tokens_missing_heads(self) -> list[UDToken]:
        return [tok for tok in self.compound.tokens if tok.head.id > self.compound.current.id]
