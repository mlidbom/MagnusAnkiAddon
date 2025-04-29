from __future__ import annotations

from typing import Callable, Union

from spacy.tokens import Token
from unidic2ud import UDPipeEntry  # type: ignore

from language_services.shared.jatoken import JAToken
from language_services.universal_dependencies.shared.tokenizing import xpos, deprel, ud_universal_part_of_speech_tag
from language_services.universal_dependencies.shared.tokenizing.ud_universal_part_of_speech_tag import UDPOS
from language_services.universal_dependencies.shared.tokenizing.xpos import XPOS

from sysutils import ex_str, kana_utils, typed

def _head(token: UDPipeEntry) -> UDPipeEntry:
    return token.head  # noqa

class UDToken(JAToken):
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
            self.xpos = xpos.get_tag(typed.str_(token.tag_))
            self.deprel = deprel.get_tag(typed.str_(token.dep_).lower())
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
            self.xpos = xpos.get_tag(typed.str_(token.xpos))
            self.deprel = deprel.get_tag(typed.str_(token.deprel))
            self.feats = typed.str_(token.feats)
            self._head_id = typed.int_(_head(token).id)
            self.head = self  # ugly hack to get python typing working in spite of the recursive nature of this class. Will be replaced with correct value by parent object.

    def __str__(self) -> str:
        return self.str_(ex_str.pad_to_length)

    # noinspection DuplicatedCode
    def __repr__(self) -> str:
        return self.str_(ex_str.pad_to_length_ui_font)

    def get_base_form(self) -> str:
        return self.lemma

    def get_surface_form(self) -> str:
        return self.form

    _pseudo_verbs_for_inflection_purposes = {"ます"}
    def is_inflectable_word(self) -> bool:
        if self.upos == UDPOS.adjective:
            return True
        if self.upos == UDPOS.verb:
            return True
        if self.xpos == XPOS.verb_bound:
            return True
        if self.lemma in self._pseudo_verbs_for_inflection_purposes:
            return True
        return False

    def str_(self, padder: Callable[[str, int], str], exclude_lemma_and_norm:bool = False) -> str:
        lemma = self.lemma if self.lemma != self.form else ""
        norm = self.norm if lemma and self.norm != lemma else ""

        result = f"""{kana_utils.pad_to_length(str(self.form), 5)}"""

        if not exclude_lemma_and_norm:
            result += (f"""{kana_utils.pad_to_length(lemma, 5)}""" +
                       f"""{kana_utils.pad_to_length(norm, 5)}""")

        result += (f"""{padder(str(self.id), 3)}""" +
                   f"""{padder(str(self.head.id), 3)}""" +
                   f"""{padder(self.deprel.description, 30)}""" +
                   f"""{padder(self.xpos.description, 30)}""" +
                   f"""{padder(self.upos.description, 30)}""" #+
                   # f"""feat:{padder(self.feats, 40)}""" +
                   # f"""deps:{self.deps}""" +
                   # f"""misc:{self.misc}"""
                   )

        return result
