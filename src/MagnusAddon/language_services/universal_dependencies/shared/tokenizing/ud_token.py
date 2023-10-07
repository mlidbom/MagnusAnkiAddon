from __future__ import annotations

from typing import Union

from spacy.tokens import Token
from unidic2ud import UDPipeEntry  # type: ignore

from language_services.universal_dependencies.shared.tokenizing import ud_japanese_part_of_speech_tag, ud_relationship_tag, ud_universal_part_of_speech_tag
from sysutils import ex_str, kana_utils, typed

def _head(token: UDPipeEntry) -> UDPipeEntry:
    return token.head  # noqa

class UDToken:
    def __init__(self, token: Union[UDPipeEntry, Token]) -> None:
        if isinstance(token, Token):
            self._wrapped = token
            self.id = typed.int_(token.i)
            self.deps = typed.str_(token.dep_).lower()
            self.misc = "UNKNOWN_FIX_ME"  # typed.str_(token.misc)
            self.form = typed.str_(token.text)
            self.norm = typed.str_(token.norm_)
            self.lemma = typed.str_(token.lemma_)
            self.upos = ud_universal_part_of_speech_tag.get_tag(typed.str_(token.pos_))
            self.xpos = ud_japanese_part_of_speech_tag.get_tag(typed.str_(token.tag_))
            self.deprel = ud_relationship_tag.get_tag(typed.str_(token.dep_).lower())
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
            self.upos = ud_universal_part_of_speech_tag.get_tag(typed.str_(token.upos))
            self.xpos = ud_japanese_part_of_speech_tag.get_tag(typed.str_(token.xpos))
            self.deprel = ud_relationship_tag.get_tag(typed.str_(token.deprel))
            self.feats = typed.str_(token.feats)
            self._head_id = typed.int_(_head(token).id)
            self.head = self  # ugly hack to get python typing working in spite of the recursive nature of this class. Will be replaced with correct value by parent object.

    def is_head_of(self, candidate: UDToken) -> bool: return self == candidate.head

    # noinspection DuplicatedCode
    def __repr__(self) -> str:
        return (f"""{kana_utils.pad_to_length(str(self.form), 5)}""" +
                f"""{kana_utils.pad_to_length(str(self.lemma), 5)}""" +
                f"""{kana_utils.pad_to_length(str(self.norm), 5)}""" +
                f"""{ex_str.pad_to_length_ui_font(str(self.id), 3)}""" +
                f"""{ex_str.pad_to_length_ui_font(str(self.head.id), 3)}""" +
                f"""{ex_str.pad_to_length_ui_font(self.deprel.description, 30)}""" +
                f"""{ex_str.pad_to_length_ui_font(self.xpos.description, 30)}""" +
                f"""{ex_str.pad_to_length_ui_font(self.upos.description, 26)}""" +
                f"""feat:{self.feats} deps:{self.deps} misc:{self.misc}""")
