from janome.tokenizer import Token
from parsing.janome_extensions.parts_of_speech import PartsOfSpeech
from sysutils import typed, kana_utils

class TokenExt:
    def __init__(self, token: Token):
        self._token = token
        self.base_form = typed.str_(token.base_form)
        self.surface = typed.str_(token.surface)
        self.inflection_type = typed.str_(token.infl_type).replace("*", "")
        self.inflected_form = typed.str_(token.infl_form).replace("*", "")
        self.base_form = typed.str_(token.base_form)
        self.reading = typed.str_(token.reading)
        self.phonetic = typed.str_(token.phonetic)
        self.node_type = typed.str_(token.node_type)
        self.parts_of_speech = PartsOfSpeech.fetch(typed.str_(token.part_of_speech))

    def __repr__(self) -> str:
        return "".join([
             "baf: " + kana_utils.pad_to_length(self.base_form, 6),
             "sur: " + kana_utils.pad_to_length(self.surface if self.surface != self.base_form else "", 6),
             "inf: " + kana_utils.pad_to_length(self.inflected_form, 6),
             "int: " + kana_utils.pad_to_length(self.inflection_type, 10),
             "pos: " + str(self.parts_of_speech)])