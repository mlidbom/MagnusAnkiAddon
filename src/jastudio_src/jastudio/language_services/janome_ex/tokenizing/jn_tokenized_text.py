from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio import mylog
from jastudio.ankiutils import app
from jastudio.language_services.janome_ex.tokenizing.pre_processing_stage.pre_processing_stage import PreProcessingStage

if TYPE_CHECKING:
    from janome.tokenizer import Token  # pyright: ignore[reportMissingTypeStubs]
    from jastudio.language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from jastudio.language_services.janome_ex.tokenizing.jn_token import JNToken

class JNTokenizedText(Slots):
    def __init__(self, text: str, raw_tokens: list[Token], tokens: list[JNToken]) -> None:
        self.raw_tokens: list[Token] = raw_tokens
        self.text: str = text
        self.tokens: list[JNToken] = tokens

    def pre_process(self) -> list[IAnalysisToken]:
        try:
            return PreProcessingStage(app.col().vocab).pre_process(self.tokens)
        except Exception:
            mylog.error(f"""Failed to pre-process text: {self.text}""")
            raise
