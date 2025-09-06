from __future__ import annotations

from typing import TYPE_CHECKING

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
    def __init__(self, surface: str, base: str, base_for_vocab: str, is_non_word_character: bool) -> None:
        self.surface = surface
        self.base_form = base
        self.base_form_for_non_compound_vocab_matching = base_for_vocab
        self.is_inflectable_word: bool = False
        self.is_non_word_character = is_non_word_character
        self.potential_godan_verb: str | None = None

    def is_past_tense_stem(self) -> bool: return False
    def is_past_tense_marker(self) -> bool: return False

    def __repr__(self) -> str:
        return f"ProcessedToken('{self.surface}', '{self.base_form}', '{self.base_form_for_non_compound_vocab_matching}', {self.is_inflectable_word})"

class JNTokenWrapper(ProcessedToken, Slots):
    def __init__(self, token: JNToken, vocabs: VocabCollection) -> None:
        super().__init__(token.surface, token.base_form, token.base_form, token.parts_of_speech.is_non_word_character())
        self.token = token
        self._vocabs = vocabs
        self.is_inflectable_word = self.token.is_inflectable_word()

    def is_past_tense_stem(self) -> bool: return self.token.is_past_tense_stem()
    def is_past_tense_marker(self) -> bool: return self.token.is_past_tense_marker()

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
