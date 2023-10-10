"""Really only exists to keep supporting logic out of the real compound builder so that it can be as readable as we're able to make it"""
from __future__ import annotations

from typing import Callable

from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken

class CompoundingRuleSet:
    def __init__(self, join_when: list[Callable[[], bool]], split_when: list[Callable[[], bool]]):
        self.join_rules = join_when
        self.split_rules = split_when


class CompoundBuilderBase:
    def __init__(self, source_tokens: list[UDToken], depth: int):
        self.source_tokens = source_tokens
        self.tokens = [source_tokens.pop(0)]
        self.depth_rules: list[CompoundingRuleSet] = []
        self.depth = depth

    @property
    def current(self) -> UDToken: return self.tokens[-1]
    @property
    def next(self) -> UDToken: return self.source_tokens[0]
    @property
    def first(self) -> UDToken: return self.tokens[0]
    @property
    def has_next(self) -> bool: return len(self.source_tokens) > 0

    def consume_next(self) -> None:
        self.tokens.append(self.source_tokens.pop(0))

    def build(self) -> list[UDToken]:
        if self.depth < len(self.depth_rules):
            join_when = self.depth_rules[self.depth].join_rules
            split_when = self.depth_rules[self.depth].split_rules
        else:
            join_when = []
            split_when = []

        while self.has_next:
            if any(rule() for rule in split_when):
                break
            if any(rule() for rule in join_when):
                self.consume_next()
            else:
                break

        return self.tokens
