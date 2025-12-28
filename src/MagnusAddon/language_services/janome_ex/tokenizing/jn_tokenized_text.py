from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.tokenizing.pre_processing_stage.pre_processing_stage import PreProcessingStage

if TYPE_CHECKING:
    from janome.tokenizer import Token  # pyright: ignore[reportMissingTypeStubs]
    from language_services.janome_ex.tokenizing.jn_token import JNToken
    from language_services.janome_ex.tokenizing.processed_token import ProcessedToken
    from typed_linq_collections.collections.q_list import QList

class JNTokenizedText(Slots):
    def __init__(self, text: str, raw_tokens: QList[Token], tokens: QList[JNToken]) -> None:
        self.raw_tokens: list[Token] = raw_tokens
        self.text: str = text
        self.tokens: QList[JNToken] = tokens

    def pre_process(self) -> QList[ProcessedToken]:
        return PreProcessingStage(app.col().vocab).pre_process(self.tokens)
