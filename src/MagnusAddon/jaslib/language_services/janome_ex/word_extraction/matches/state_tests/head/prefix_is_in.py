from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsPrefixIsIn(Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        prefixes = inspector.match.rules.prefix_is_not.get()
        if prefixes and any(prefix for prefix in prefixes if inspector.prefix.endswith(prefix)):
            return FailedMatchRequirement.forbids(f"""prefix_in:{",".join(prefixes)}""")

        return None

class RequiresPrefixIsIn(Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        prefixes = inspector.match.rules.required_prefix.get()
        if prefixes and not any(prefix for prefix in prefixes if inspector.prefix.endswith(prefix)):
            return FailedMatchRequirement.required(f"""prefix_in:{",".join(prefixes)}""")

        return None
