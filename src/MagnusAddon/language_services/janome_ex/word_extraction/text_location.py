from typing import Optional

from language_services.janome_ex.tokenizing.jn_token import JNToken

class TextLocation:
    def __init__(self, start_index:int, surface:str, base:str):
        self.start_index = start_index
        self.end_index = start_index + len(surface) - 1
        self.surface = surface
        self.base = base
        self.previous:Optional[TextLocation] = None
        self.next: Optional[TextLocation] = None

    def __repr__(self) -> str:
        return f"TextLocation('{self.start_index}-{self.end_index}, {self.surface} | {self.base}  prev.start:{self.previous.start_index if self.previous else None}, next.start:{self.next.start_index if self.next else None})"

class TokenTextLocation(TextLocation):
    def __init__(self, token: JNToken, start_index:int):
        super().__init__(start_index, token.surface, token.base_form)
        self.token = token
