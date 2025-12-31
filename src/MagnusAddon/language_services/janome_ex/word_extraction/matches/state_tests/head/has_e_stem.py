from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services import conjugator
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids
from sysutils import kana_utils

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsHasEStem(CustomRequiresOrForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def is_required(self) -> bool:
        return self.inspector.match.requires_forbids.e_stem.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.inspector.match.requires_forbids.e_stem.is_forbidden

    @property
    @override
    def description(self) -> str: return "e_stem"

    @override
    def _internal_is_in_state(self) -> bool:
        if not self.inspector.prefix:
            return False

        if self.inspector.prefix[-1] in conjugator.e_stem_characters:
            return True

        if kana_utils.character_is_kanji(self.inspector.prefix[-1]):  # noqa: SIM103
            return True
        return False
