from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils import app
from ex_autoslot import AutoSlots
from language_services import conjugator
from language_services.jamdict_ex.dict_lookup import DictLookup

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
        self.is_potential_godan: bool = is_potential_godan

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

    def pre_process(self) -> list[ProcessedToken]:
        potential_godan_verb: str | None = self._try_find_vocab_based_potential_verb_compound() or self._try_find_dictionary_based_potential_godan_verb()
        if potential_godan_verb is not None:
            return self._split_potential_or_imperative_godan(potential_godan_verb)
        return [self]

    def _split_potential_or_imperative_godan(self, godan_base: str) -> list[ProcessedToken]:
        if not self.surface.endswith("る"): #this is not the dictionary form of the potential part  # noqa: SIM102
            if self.token.next is None or not self.token.next.is_valid_potential_form_inflection():  # this is an imperative
                return [ProcessedToken(surface=self.surface, base=godan_base, is_non_word_character=False, is_inflectable_word=True)]

        godan_surface = self.surface.removesuffix("る")[:-1]
        potential_stem = self.surface.removesuffix("る")[-1]
        potential_base = potential_stem + "る"
        return [ProcessedToken(surface=godan_surface, base=godan_base, is_non_word_character=False, is_inflectable_word=True),
                ProcessedToken(surface=potential_stem, base=potential_base, is_non_word_character=False, is_inflectable_word=True, is_potential_godan=True)]

    def _try_find_vocab_based_potential_verb_compound(self) -> str | None:
        for vocab in self._vocabs.with_question(self.base_form):
            compound_parts = vocab.compound_parts.all()
            if len(compound_parts) == 2 and compound_parts[1] == "える":
                return compound_parts[0]
        return None

    def _try_find_dictionary_based_potential_godan_verb(self) -> str | None:
        if (len(self.token.base_form) >= 2
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
