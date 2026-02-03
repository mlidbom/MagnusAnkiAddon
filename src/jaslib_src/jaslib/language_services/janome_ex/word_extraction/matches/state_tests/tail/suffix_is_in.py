from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsSuffixIsIn(Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        suffixes = inspector.match.rules.suffix_is_not.get()
        if suffixes and any(suffix for suffix in suffixes if inspector.suffix.startswith(suffix)):
            return FailedMatchRequirement.forbids(f"""suffix_in:{",".join(suffixes)}""")

        return None
