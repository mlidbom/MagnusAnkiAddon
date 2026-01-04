from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from typed_linq_collections.collections.q_set import QSet

class ForbidsPrefixIsIn(Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector, prefixes: QSet[str]) -> MatchRequirement | None:
        if prefixes and any(prefix for prefix in prefixes if inspector.prefix.endswith(prefix)):
            return FailedMatchRequirement.forbids(f"""prefix_in:{",".join(prefixes)}""")

        return None

class RequiresPrefixIsIn(Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector, prefixes: QSet[str]) -> MatchRequirement | None:
        if prefixes and not any(prefix for prefix in prefixes if inspector.prefix.endswith(prefix)):
            return FailedMatchRequirement.required(f"""prefix_in:{",".join(prefixes)}""")

        return None
