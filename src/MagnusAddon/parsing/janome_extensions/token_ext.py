from janome.tokenizer import Token
from parsing.janome_extensions.parts_of_speech import PartsOfSpeech
from sysutils import typed

class TokenExt:
    def __init__(self, token: Token):
        self._token = token
        self.base_form = typed.str_(token.base_form)
        self.surface = typed.str_(token.surface)
        self.inflection_type = typed.str_(token.infl_type)
        self.inflected_form = typed.str_(token.infl_form)
        self.base_form = typed.str_(token.base_form)
        self.reading = typed.str_(token.reading)
        self.phonetic = typed.str_(token.phonetic)
        self.node_type = typed.str_(token.node_type)
        self.part_of_speech = typed.str_(token.part_of_speech)
        self.parts_of_speech = PartsOfSpeech(self.part_of_speech)

    def __str__(self) -> str: return self._token.__str__()