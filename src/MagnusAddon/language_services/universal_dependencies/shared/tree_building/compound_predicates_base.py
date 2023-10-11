from __future__ import annotations

from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tree_building.compound_builder_base import CompoundBuilderBase

class CompoundPredicatesBase:
    def __init__(self, compound: CompoundBuilderBase):
        self.compound = compound

    @property
    def _current(self) -> UDToken: return self.compound.current
    @property
    def _tokens(self) -> list[UDToken]: return self.compound.tokens
    @property
    def _next(self) -> UDToken: return self.compound.next
    @property
    def _source_tokens(self) -> list[UDToken]: return self.compound.source_tokens
