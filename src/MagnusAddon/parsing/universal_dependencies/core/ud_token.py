from typing import Union

from spacy.tokens import Token
from unidic2ud import UDPipeEntry

from parsing.universal_dependencies.core import ud_japanese_part_of_speech_tag, ud_universal_part_of_speech_tag, ud_relationship_tag
from sysutils import typed, kana_utils


def _head(token:UDPipeEntry) -> UDPipeEntry:
    return token.head # noqa

_missing_value = "_"

class UDToken:
    def __init__(self, token: Union[UDPipeEntry, Token]) -> None:

        if isinstance(token, Token):
            self._wrapped = token
            self.id = typed.int_(token.i)
            self.deps = typed.str_(token.dep_).lower()
            self.misc = "UNKNOWN_FIX_ME" # typed.str_(token.misc)
            self.form = typed.str_(token.text)

            # todo: think about this. it has lemma_ but that does not seem to map to kanji, while norm_ does...
            # lemma is often empty and I always LIKE that it is when it is. It is only populated when I would not find the correct value in a dictionary based on the surface.
            # norm_ on the other hand seems to always be populated whenever it can be figured out.
            # for now. let's try to populated lemma with the norm_ but only if lemma_ differs from form or norm_ contains kanji
            self.norm = typed.str_(token.norm_)
            self.lemma_real = typed.str_(token.lemma_)
            self.lemma = self.norm if self.lemma_real != self.form or not kana_utils.is_only_kana(self.norm) else self.lemma_real



            self.upos = ud_universal_part_of_speech_tag.get_tag(typed.str_(token.pos_)) if token.pos_ != _missing_value else None
            self.xpos = ud_japanese_part_of_speech_tag.get_tag(typed.str_(token.tag_)) if token.tag_ != _missing_value else None
            self.deprel = ud_relationship_tag.get_tag(typed.str_(token.dep_).lower()) if token.dep_ != _missing_value else None
            self.feats = str(token.morph)
            self._head_id = typed.int_(token.head.i)
            self.head = self  # ugly hack to get python typing working in spite of the recursive nature of this class. Will be replaced with correct value by parent object.

        if isinstance(token, UDPipeEntry):
            self._wrapped = token
            self.id = typed.int_(token.id)
            self.deps = typed.str_(token.deps)
            self.misc = typed.str_(token.misc)
            self.form = typed.str_(token.form)

            self.norm = typed.str_(token.lemma)
            self.lemma = typed.str_(token.lemma)
            self.upos = ud_universal_part_of_speech_tag.get_tag(typed.str_(token.upos)) if token.upos != _missing_value else None
            self.xpos = ud_japanese_part_of_speech_tag.get_tag(typed.str_(token.xpos)) if token.xpos != _missing_value else None
            self.deprel = ud_relationship_tag.get_tag(typed.str_(token.deprel)) if token.deprel != _missing_value else None
            self.feats = typed.str_(token.feats)
            self._head_id = typed.int_(_head(token).id)
            self.head = self #ugly hack to get python typing working in spite of the recursive nature of this class. Will be replaced with correct value by parent object.
