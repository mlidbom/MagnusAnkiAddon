# from __future__ import annotations
#
# from typing import override
#
# from autoslot import Slots
#
# from jaslib.language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
#
#
# class FailedMatchRequirement(MatchRequirement, Slots):
#     def __init__(self, reason: str) -> None:
#         self.reason: str = reason
#
#     @property
#     @override
#     def failure_reason(self) -> str: return self.reason
#
#     @property
#     @override
#     def is_fulfilled(self) -> bool: return False
#
#     @classmethod
#     def forbids(cls, message: str) -> FailedMatchRequirement: return FailedMatchRequirement(f"forbids::{message}")
#
#     @classmethod
#     def required(cls, message: str) -> FailedMatchRequirement: return FailedMatchRequirement(f"required::{message}")
