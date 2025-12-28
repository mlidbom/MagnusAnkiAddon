from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.processed_token import ProcessedToken
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken
    from note.collection.vocab_collection import VocabCollection

class IchidanGodanPotentialOrImperativeHybridSplitter(Slots):
    def __init__(self, token: JNToken, vocabs: VocabCollection) -> None:
        self.token: JNToken = token
        self._vocabs: VocabCollection = vocabs

    def try_split(self) -> list[ProcessedToken] | None:
        hidden_godan = self._try_find_godan_hidden_in_ichidan_using_dictionary() or self._try_find_vocab_based_potential_or_imperative_godan_compound()
        if hidden_godan is not None:
            if self._is_potential_godan(hidden_godan):
                return self._split_godan_potential(hidden_godan)
            if self._is_imperative_godan(hidden_godan):
                return self._split_godan_imperative(hidden_godan)

        return None

    def _split_godan_imperative(self, godan_base: str) -> list[ProcessedToken]:
        if self.token.inflected_form == InflectionForms.ImperativeMeireikei.yo:  # handles cases like 放せよ which janome turns into a single token and believes is an ichidan よ imperative
            godan_surface = self.token.surface[:-2]
            imperative_part = self.token.surface[-2]
            return [ProcessedToken(surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_imperative_stem=True),
                    ProcessedToken(surface=imperative_part, base="え", is_inflectable_word=True, is_godan_imperative_inflection=True),
                    ProcessedToken(surface="よ", base="よ", is_inflectable_word=False)]
        elif self.token.inflected_form == InflectionForms.ImperativeMeireikei.ro:  # noqa: RET505
            raise Exception("I doubt this ever happens, but let's explode if it does so we can add support")
        else:  # noqa: RET505
            godan_surface = self.token.surface[:-1]
            imperative_part = self.token.surface[-1]
            imperative_base = "い" if imperative_part == "い" else "え"
            return [ProcessedToken(surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_imperative_stem=True),
                    ProcessedToken(surface=imperative_part, base=imperative_base, is_inflectable_word=True, is_godan_imperative_inflection=True)]

    def _split_godan_potential(self, godan_base: str) -> list[ProcessedToken]:
        godan_surface = self.token.surface.removesuffix("る")[:-1]
        potential_surface = self.token.surface.removeprefix(godan_surface)
        potential_base = potential_surface if potential_surface[-1] == "る" else potential_surface + "る"

        return [ProcessedToken(surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_potential_stem=True),
                ProcessedToken(surface=potential_surface, base=potential_base, is_inflectable_word=True, is_godan_potential_inflection=True)]

    _potential_or_imperative_godan_last_compound_parts: set[str] = {"える", "え"}
    def _try_find_vocab_based_potential_or_imperative_godan_compound(self) -> str | None:
        for vocab in self._vocabs.with_question(self.token.base_form):
            compound_parts = vocab.compound_parts.all()
            if len(compound_parts) == 2 and compound_parts[1] in self._potential_or_imperative_godan_last_compound_parts:
                return compound_parts[0]
        return None

    def _is_potential_godan(self, godan_base: str) -> bool:
        if self.token.surface.endswith("る") or (self.token.next is not None and self.token.next.is_valid_potential_form_inflection()):  # noqa: SIM103
            godan_dict_entry = non_optional(DictLookup.lookup_word(godan_base).try_get_godan_verb())
            if (godan_dict_entry.is_intransitive_verb() and self.token.previous is not None and self.token.previous.surface == "を"  # intransitive verbs don't take を so this is most likely actually the ichidan verb  # noqa: SIM103
                    and DictLookup.lookup_word(self.token.base_form).try_get_ichidan_verb() is not None):  # if one actally exists in the dictionary, if not this is most likely one of the godan verbs of motion that use を to refer to the space traversed
                return False
            return True
        return False

    def _is_imperative_godan(self, godan_base: str) -> bool:
        godan_dict_entry = non_optional(DictLookup.lookup_word(godan_base).try_get_godan_verb())
        ichidan_verb = DictLookup.lookup_word(self.token.base_form).try_get_ichidan_verb()
        if ichidan_verb is None:
            return True  # we check for potential godan before this, so if there is no ichidan verb in the dictonary, the only thing left is an imperative godan
        elif godan_dict_entry.is_intransitive_verb() and self.token.previous is not None and self.token.previous.surface == "を":  # intransitive verbs don't take を so this is most likely actually the ichidan verb  # noqa: RET505, SIM103
            return False
        elif self.token.next is None or self.token.is_end_of_statement():  # noqa: SIM114
            return True
        elif self.token.inflected_form == InflectionForms.ImperativeMeireikei.yo:  # handles cases like 放せよ which janome turns into a single token and believes is an ichidan よ imperative
            return True

        return False

    def _try_find_godan_hidden_in_ichidan_using_dictionary(self) -> str | None:
        if (len(self.token.base_form) >= 2
                and self.token.base_form[-2:] in conjugator.godan_potential_verb_ending_to_dictionary_form_endings
                and self.token.is_ichidan_verb()):
            possible_godan_form = conjugator.construct_root_verb_for_possibly_potential_godan_verb_dictionary_form(self.token.base_form)
            if DictLookup.lookup_word(possible_godan_form).try_get_godan_verb() is not None:
                return possible_godan_form
        return None


