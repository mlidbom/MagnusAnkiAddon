from janome.tokenizer import Token


class TokenExt:
    def __init__(self, token: Token):
        self._token = token
        self.base_form = token.base_form
        self.surface = token.surface
        self.part_of_speech = token.part_of_speech
        self.inflection_type = token.infl_type
        self.inflected_form = token.infl_form
        self.base_form = token.base_form
        self.reading = token.reading
        self.phonetic = token.phonetic
        self.node_type = token.node_type

    def __str__(self) -> str: return self._token.__str__()