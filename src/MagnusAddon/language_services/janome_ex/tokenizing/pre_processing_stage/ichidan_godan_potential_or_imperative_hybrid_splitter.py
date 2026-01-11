from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from language_services.janome_ex.tokenizing.godan_dictionary_form_stem import GodanPotentialDictionaryFormInflection
from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.pre_processing_stage.word_info import WordInfo
from language_services.janome_ex.tokenizing.split_token import SplitToken
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from language_services.janome_ex.tokenizing.jn_token import JNToken
    from note.collection.vocab_collection import VocabCollection
    from note.vocabulary.vocabnote import VocabNote

class IchidanGodanPotentialOrImperativeHybridSplitter(Slots):

    @classmethod
    def try_split(cls, token: JNToken, vocabs: VocabCollection) -> list[IAnalysisToken] | None:
        if token.inflected_form == InflectionForms.ImperativeMeireikei.ro:
            return None

        hidden_godan = cls._try_find_godan_hidden_in_ichidan_using_dictionary(token) or cls._try_find_vocab_based_potential_or_imperative_godan_compound(token, vocabs)
        if hidden_godan is not None:
            if cls._is_potential_godan(token, hidden_godan):
                return cls._split_godan_potential(token, hidden_godan)
            if cls._is_imperative_godan(token, hidden_godan):
                return cls._split_godan_imperative(token, hidden_godan)

        return None

    @classmethod
    def _split_godan_imperative(cls, token: JNToken, godan_base: str) -> list[IAnalysisToken]:
        if token.inflected_form == InflectionForms.ImperativeMeireikei.yo:  # handles cases like 放せよ which janome turns into a single token and believes is an ichidan よ imperative
            godan_surface = token.surface[:-2]
            imperative_part = token.surface[-2]
            return [SplitToken(token, surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_imperative_stem=True),
                    SplitToken(token, surface=imperative_part, base="え", is_inflectable_word=True, is_godan_imperative_inflection=True),
                    SplitToken(token, surface="よ", base="よ", is_inflectable_word=False)]
        else:  # noqa: RET505
            godan_surface = token.surface[:-1]
            imperative_part = token.surface[-1]
            imperative_base = "い" if imperative_part == "い" else "え"
            return [SplitToken(token, surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_imperative_stem=True),
                    SplitToken(token, surface=imperative_part, base=imperative_base, is_inflectable_word=True, is_godan_imperative_inflection=True)]

    @classmethod
    def _split_godan_potential(cls, token: JNToken, godan_base: str) -> list[IAnalysisToken]:
        is_dictionary_form = token.surface[-1] == "る"

        godan_surface = token.surface.removesuffix("る")[:-1]
        potential_surface = token.surface.removeprefix(godan_surface)
        potential_base = potential_surface if is_dictionary_form else potential_surface + "る"

        if is_dictionary_form:
            potential_surface = potential_surface[:-1]
            return [SplitToken(token, surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_potential_stem=True),
                    SplitToken(token, surface=potential_surface, base=potential_base, is_inflectable_word=True, is_godan_potential_inflection=True),
                    GodanPotentialDictionaryFormInflection(token)]

        return [SplitToken(token, surface=godan_surface, base=godan_base, is_inflectable_word=True, is_godan_potential_stem=True),
                SplitToken(token, surface=potential_surface, base=potential_base, is_inflectable_word=True, is_godan_potential_inflection=True)]

    _potential_or_imperative_godan_last_compound_parts: set[str] = {"える", "え"}
    @classmethod
    def _try_find_vocab_based_potential_or_imperative_godan_compound(cls, token: JNToken, vocabs: VocabCollection) -> str | None:
        for vocab in vocabs.with_question(token.base_form):
            compound_parts = vocab.compound_parts.all()
            if len(compound_parts) == 2 and compound_parts[1] in cls._potential_or_imperative_godan_last_compound_parts:  # noqa: SIM102
                if WordInfo.is_godan(compound_parts[0]):
                    return compound_parts[0]
        return None

    @classmethod
    def _is_potential_godan(cls, token: JNToken, godan_base: str) -> bool:
        if token.surface.endswith("る") or (token.next is not None and token.next.is_valid_godan_potential_form_inflection()):  # noqa: SIM103
            godan_dict_entry = non_optional(WordInfo.lookup_godan(godan_base))
            if (godan_dict_entry.is_intransitive and token.previous is not None and token.previous.surface == "を"  # intransitive verbs don't take を so this is most likely actually the ichidan verb  # noqa: SIM103
                    and WordInfo.is_ichidan(token.base_form)):  # if one actally exists in the dictionary, if not this is most likely one of the godan verbs of motion that use を to refer to the space traversed
                return False
            return True
        return False

    @classmethod
    def _is_imperative_godan(cls, token: JNToken, godan_base: str) -> bool:
        if token.surface[-1] not in conjugator.godan_imperative_verb_endings and token.inflected_form != InflectionForms.ImperativeMeireikei.yo:
            return False
        godan_word_info = WordInfo.lookup(godan_base)
        if WordInfo.lookup(token.base_form) is None:
            return True  # we check for potential godan before this, so if there is no ichidan verb in the dictonary, the only thing left is an imperative godan
        elif (godan_word_info is not None and godan_word_info.is_intransitive) and token.previous is not None and token.previous.surface == "を":  # intransitive verbs don't take を so this is most likely actually the ichidan verb  # noqa: RET505, SIM103
            return False
        elif token.next and token.next.cannot_follow_ichidan_stem():  # noqa: SIM114
            return True
        elif token.next is None or token.is_end_of_statement:  # noqa: SIM114
            return True
        elif token.inflected_form == InflectionForms.ImperativeMeireikei.yo:  # handles cases like 放せよ which janome turns into a single token and believes is an ichidan よ imperative  # noqa: SIM114
            return True
        elif token.next and token.next.is_more_likely_to_follow_imperative_than_ichidan_stem():  # noqa: SIM114
            return True

        return False

    @classmethod
    def base_form_has_godan_potential_ending(cls, base_form: str) -> bool:
        return base_form[-2:] in conjugator.godan_potential_verb_ending_to_dictionary_form_endings

    @classmethod
    def _try_find_godan_hidden_in_ichidan_using_dictionary(cls, token: JNToken) -> str | None:
        if (len(token.base_form) >= 2
                and cls.base_form_has_godan_potential_ending(token.base_form)
                and token.is_ichidan_verb):
            possible_godan_form = conjugator.construct_root_verb_for_possibly_potential_godan_verb_dictionary_form(token.base_form)
            if WordInfo.is_godan(possible_godan_form):
                return possible_godan_form
        return None

    @classmethod
    def is_ichidan_hiding_godan(cls, vocab: VocabNote) -> bool:
        question = vocab.get_question()
        if cls.base_form_has_godan_potential_ending(question):
            possible_godan_form = conjugator.construct_root_verb_for_possibly_potential_godan_verb_dictionary_form(question)
            godan_dict_entry = WordInfo.lookup_godan(possible_godan_form)
            if godan_dict_entry is not None and godan_dict_entry.is_godan:  # noqa: SIM103
                return True
            return False
        return False
