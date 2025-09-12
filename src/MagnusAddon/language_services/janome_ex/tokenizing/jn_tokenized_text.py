from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils import app
from autoslot import Slots
from language_services import conjugator
from language_services.jamdict_ex.dict_lookup import DictLookup
from sysutils import ex_sequence

if TYPE_CHECKING:
    from janome.tokenizer import Token
    from language_services.janome_ex.tokenizing.jn_token import JNToken
    from note.collection.vocab_collection import VocabCollection

class ProcessedToken(Slots):
    def __init__(self, surface: str, base: str, is_non_word_character: bool) -> None:
        self.surface = surface
        self.base_form = base
        self.is_inflectable_word: bool = False
        self.is_non_word_character = is_non_word_character
        self.potential_godan_verb: str | None = None

    def is_past_tense_stem(self) -> bool: return False
    def is_ichidan_masu_stem(self) -> bool: return False
    def is_t_form_stem(self) -> bool: return False
    def is_past_tense_marker(self) -> bool: return False
    def is_special_nai_negative(self) -> bool: return False

    @override
    def __repr__(self) -> str:
        return f"ProcessedToken('{self.surface}', '{self.base_form}', {self.is_inflectable_word})"

class JNTokenWrapper(ProcessedToken, Slots):
    def __init__(self, token: JNToken, vocabs: VocabCollection) -> None:
        super().__init__(token.surface, token.base_form, token.parts_of_speech.is_non_word_character())
        self.token = token
        self._vocabs = vocabs
        self.is_inflectable_word = self.token.is_inflectable_word()

    @override
    def is_past_tense_stem(self) -> bool: return self.token.is_past_tense_stem()
    @override
    def is_t_form_stem(self) -> bool: return self.token.is_t_form_stem()
    @override
    def is_ichidan_masu_stem(self) -> bool: return self.token.is_ichidan_masu_stem()
    @override
    def is_past_tense_marker(self) -> bool: return self.token.is_past_tense_marker()
    @override
    def is_special_nai_negative(self) -> bool: return self.token.is_special_nai_negative()

    # todo: restore the splitting of godan verbs, but this time around:
    #  1. output a first token that has the whole current surface, but with the normal Godan as it's base, along with the metadata that this is a potential godan stem token.
    #  2. output a second token with an EMPTY surface and a base that is える. Via the base the potential compound will be matched later.
    #  3. add a fallback/alternative surface member to ProcessedToken. For potential godans that will be え.
    #  4. When a CandidateWord encounters an empty form at the start of it's token chain, it will replace it with the alternative surface,
    #     thus effectively creating an alternative repretation of that index in the analysis, since the next token starts at the same index.
    #  5. All that would have been matched before will be matched normally from the next token, while the potential token/location will allow any compounds starting with e
    #   and marked as requiring a potential godan stem, to correctly match all the potential conjugations.
    #  6. A configuration option can determine whether the matches from the original surface or the alternative surface should be the ones used in the display,
    #    in the indexing both will of course always be output so that all the sentences containing える will be correctly identified.
    #  7. Note, when calculating shadowing the empty tokens must not be counted, or words that are actually shadowed will be displayed.
    def pre_process(self) -> list[ProcessedToken]:
        self.potential_godan_verb = self._try_find_vocab_based_potential_verb_compound() or self._try_find_dictionary_based_potential_godan_verb()
        return [self]

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

class JNTokenizedText(Slots):
    def __init__(self, text: str, raw_tokens: list[Token], tokens: list[JNToken]) -> None:
        self.raw_tokens = raw_tokens
        self.text = text
        self.tokens = tokens

    def pre_process(self) -> list[ProcessedToken]:
        vocab = app.col().vocab

        step1 = [JNTokenWrapper(token, vocab) for token in self.tokens]
        return ex_sequence.flatten([token.pre_process() for token in step1])
