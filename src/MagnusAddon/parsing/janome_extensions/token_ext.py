from janome.tokenizer import Token
from parsing.janome_extensions.parts_of_speech import PartsOfSpeech
from sysutils import typed, kana_utils

class TokenExt:
    def __init__(self,
                 base_form: str,
                 surface:str,
                 inflection_type: str,
                 inflected_form,
                 reading:str,
                 phonetic:str,
                 node_type:str,
                 parts_of_speech: PartsOfSpeech):
        self.base_form = typed.str_(base_form)
        self.surface = typed.str_(surface)
        self.inflection_type = typed.str_(inflection_type).replace("*", "")
        self.inflected_form = typed.str_(inflected_form).replace("*", "")
        self.reading = typed.str_(reading)
        self.phonetic = typed.str_(phonetic)
        self.node_type = typed.str_(node_type)
        self.parts_of_speech = parts_of_speech

    def __repr__(self) -> str:
        return "".join([
             "baf: " + kana_utils.pad_to_length(self.base_form, 6),
             "sur: " + kana_utils.pad_to_length(self.surface if self.surface != self.base_form else "", 6),
             "inf: " + kana_utils.pad_to_length(self.inflected_form, 6),
             "int: " + kana_utils.pad_to_length(self.inflection_type, 10),
             "pos: " + str(self.parts_of_speech)])