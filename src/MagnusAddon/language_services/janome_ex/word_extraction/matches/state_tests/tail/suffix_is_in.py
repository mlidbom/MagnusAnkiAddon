from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from typed_linq_collections.collections.q_set import QSet

class ForbidsSuffixIsIn(Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector, suffixes: QSet[str]) -> FailedMatchRequirement | None:
        if suffixes and any(suffix for suffix in suffixes if inspector.suffix.startswith(suffix)):
            return FailedMatchRequirement.forbids(f"""suffix_in:{",".join(suffixes)}""")

        return None
