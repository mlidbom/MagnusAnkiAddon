from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils import app
from ex_autoslot import AutoSlots
from language_services import conjugator
from language_services.jamdict_ex.dict_lookup import DictLookup
from sysutils import typed

if TYPE_CHECKING:
    from janome.tokenizer import Token  # pyright: ignore[reportMissingTypeStubs]
    from language_services.janome_ex.tokenizing.jn_token import JNToken
    from note.collection.vocab_collection import VocabCollection
    from typed_linq_collections.collections.q_list import QList

class ProcessedToken(AutoSlots):
    def __init__(self, surface: str, base: str, is_non_word_character: bool, is_inflectable_word: bool = False, is_potential_godan: bool = False) -> None:
        self.surface: str = surface
        self.base_form: str = base
        self.is_inflectable_word: bool = is_inflectable_word
        self.is_non_word_character: bool = is_non_word_character
        self.potential_godan_verb: str | None = None
        self.is_potential_godan:bool = is_potential_godan

    def is_past_tense_stem(self) -> bool: return False
    def is_ichidan_masu_stem(self) -> bool: return False
    def is_te_form_stem(self) -> bool: return False
    def is_past_tense_marker(self) -> bool: return False
    def is_special_nai_negative(self) -> bool: return False

    @override
    def __repr__(self) -> str:
        return f"ProcessedToken('{self.surface}', '{self.base_form}', {self.is_inflectable_word})"

class JNTokenWrapper(ProcessedToken, AutoSlots):
    def __init__(self, token: JNToken, vocabs: VocabCollection) -> None:
        super().__init__(token.surface, token.base_form, token.parts_of_speech.is_non_word_character())
        self.token: JNToken = token
        self._vocabs: VocabCollection = vocabs
        self.is_inflectable_word: bool = self.token.is_inflectable_word()

    @override
    def is_past_tense_stem(self) -> bool: return self.token.is_past_tense_stem()
    @override
    def is_te_form_stem(self) -> bool: return self.token.is_te_form_stem()
    @override
    def is_ichidan_masu_stem(self) -> bool: return self.token.is_ichidan_masu_stem()
    @override
    def is_past_tense_marker(self) -> bool: return self.token.is_past_tense_marker()
    @override
    def is_special_nai_negative(self) -> bool: return self.token.is_special_nai_negative()

    # todo: restore the splitting of godan verbs, but this time around:
    # Move the え sound to a separate token instead of keeping it in the verb stem in the way that is linguistically correct. We don't care about that, we care about being able to create breakdowns including potential forms and their conjugations.
    # So, for example, 作れた will be tokenized as:
    #   surfaces: 作 　れ 　た
    #      bases: 作る れる た
    # this should result in pretty much everything just working, as long as the potential conjugations have a form for each consonant, える, ける, せる, てる, ねる, へる, める,　れる, げる, ぜる, でる, べる, ぺる
    # see AI chat here: https://www.perplexity.ai/search/jue-dui-niaiturawojiang-fu-sas-P7TjirP4QSyOpAHP.UJKcQ (the programming discussion starts quite a bit down in the chat)
    #
    #   Legacy idea that is much more complicated:
    #       1. output a first token that has the whole current surface, but with the normal Godan as it's base, along with the metadata that this is a potential godan stem token.
    #       2. output a second token with an EMPTY surface and a base that is える. Via the base the potential compound will be matched later.
    #       3. add a fallback/alternative surface member to ProcessedToken. For potential godans that will be え.
    #       4. When a CandidateWord encounters an empty form at the start of it's token chain, it will replace it with the alternative surface,
    #           thus effectively creating an alternative repretation of that index in the analysis, since the next token starts at the same index.
    #       5. All that would have been matched before will be matched normally from the next token, while the potential token/location will allow any compounds starting with e
    #           and marked as requiring a potential godan stem, to correctly match all the potential conjugations.
    #       6. A configuration option can determine whether the matches from the original surface or the alternative surface should be the ones used in the display,
    #           in the indexing both will of course always be output so that all the sentences containing える will be correctly identified.
    #       7. Note, when calculating shadowing the empty tokens must not be counted, or words that are actually shadowed will be displayed.
    def pre_process(self) -> list[ProcessedToken]:
        self.potential_godan_verb: str | None = self._try_find_vocab_based_potential_verb_compound() or self._try_find_dictionary_based_potential_godan_verb()
        # if self.potential_godan_verb is not None:
        #     return self._split_potential_godan()
        return [self]

    def _split_potential_godan(self) -> list[ProcessedToken]:
        godan_base = typed.non_optional(self.potential_godan_verb)
        godan_surface = godan_base[:-1]

        potential_surface = self.surface[len(godan_surface):]
        potential_base = potential_surface
        if not potential_base.endswith("る"):
            potential_base = potential_surface + "る"

        return [ProcessedToken(surface=godan_surface, base=godan_base, is_non_word_character=False, is_inflectable_word=True),
                ProcessedToken(surface=potential_surface, base=potential_base, is_non_word_character=False, is_inflectable_word=True, is_potential_godan=True)]

    def _try_find_vocab_based_potential_verb_compound(self) -> str | None:
        for vocab in self._vocabs.with_question(self.base_form):
            compound_parts = vocab.compound_parts.all()
            if len(compound_parts) == 2 and compound_parts[1] == "える":
                return compound_parts[0]
        return None

    def _try_find_dictionary_based_potential_godan_verb(self) -> str | None:
        if (len(self.token.base_form) >= 3
                and self.token.base_form[-2:] in conjugator.godan_potential_verb_ending_to_dictionary_form_endings
                and self.token.is_ichidan_verb()
                and not DictLookup.is_word(self.token.base_form)):  # the potential verbs are generally not in the dictionary this is how we know them
            root_verb = conjugator.construct_root_verb_for_possibly_potential_godan_verb_dictionary_form(self.token.base_form)
            if DictLookup.is_word(root_verb):
                lookup = DictLookup.lookup_word(root_verb)
                if lookup.found_words():
                    is_godan = any(e for e in lookup.entries if "godan verb" in e.parts_of_speech())
                    if not is_godan:
                        return None
                return root_verb
        return None

class JNTokenizedText(AutoSlots):
    def __init__(self, text: str, raw_tokens: QList[Token], tokens: QList[JNToken]) -> None:
        self.raw_tokens: list[Token] = raw_tokens
        self.text: str = text
        self.tokens: QList[JNToken] = tokens

    def pre_process(self) -> QList[ProcessedToken]:
        vocab = app.col().vocab

        return self.tokens.select_many(lambda token: JNTokenWrapper(token, vocab).pre_process()).to_list()
        # query(JNTokenWrapper(token, vocab) for token in self.tokens)
        # return ex_sequence.flatten([token.pre_process() for token in step1])
