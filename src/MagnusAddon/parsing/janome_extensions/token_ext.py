from janome.tokenizer import Token
from parsing.janome_extensions.parts_of_speech import PartsOfSpeech
from sysutils import typed
from wcwidth import wcswidth

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
        self.parts_of_speech = PartsOfSpeech(typed.str_(token.part_of_speech))

    def __repr__(self) -> str:
        #Tries to make the string length such that we more or less line up the : characters in the debugger display
        def ml(value:str, max_length: int) -> str:
            actual_width = int(wcswidth(value) * 1.7)
            padding_length = max_length - actual_width
            return f"{value:.{max_length}}" + ' ' * padding_length

        return ":".join([ml(self.surface, 20),
                         ml(self.base_form, 20),
                         ml(self.inflected_form, 20),
                         ml(self.inflection_type, 30),
                         str(self.parts_of_speech)])