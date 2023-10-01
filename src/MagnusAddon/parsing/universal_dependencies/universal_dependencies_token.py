from unidic2ud import UDPipeEntry

from parsing.universal_dependencies import ud_japanese_part_of_speech_tag, ud_relationship_tag, ud_universal_part_of_speech_tag
from sysutils import typed

def _head(token:UDPipeEntry) -> UDPipeEntry:
    return token.head # noqa

class UD2UDToken:
    def __init__(self, token: UDPipeEntry) -> None:
        self.lemma = typed.str_(token.lemma)
        self.form = typed.str_(token.form)
        self.upos = ud_universal_part_of_speech_tag.get_tag(typed.str_(token.upos))
        self.xpos = ud_japanese_part_of_speech_tag.get_tag(typed.str_(token.xpos))
        self.deprel = ud_relationship_tag.get_tag(type.__str__(token.deprel))
        self.feats = typed.str_(token.feats)
        self.head_id = typed.int_(_head(token).id)