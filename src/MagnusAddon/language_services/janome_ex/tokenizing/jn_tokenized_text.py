from language_services import conjugator
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.tokenizing.jn_token import JNToken
from mylog import log
from note.collection.vocab_collection import VocabCollection
from sysutils import ex_sequence


class ProcessedToken:
    def __init__(self, surface: str, base: str, base_for_vocab: str) -> None:
        self.surface = surface
        self.base_form = base
        self.base_form_for_non_compound_vocab_matching = base_for_vocab
        self.is_inflectable_word: bool = False
        self.do_not_match_surface_for_non_compound_vocab: bool = False

    def __repr__(self) -> str:
        return f"ProcessedToken('{self.surface}', '{self.base_form}', '{self.base_form_for_non_compound_vocab_matching}', {self.is_inflectable_word})"

class SplitToken(ProcessedToken):
    def __init__(self, surface: str, base: str, base_for_vocab: str, is_inflectable_word: bool, do_not_match_surface_for_non_compound_vocab: bool) -> None:
        super().__init__(surface, base, base_for_vocab)
        self.is_inflectable_word = is_inflectable_word
        self.do_not_match_surface_for_non_compound_vocab = do_not_match_surface_for_non_compound_vocab

class JNTokenWrapper(ProcessedToken):
    def __init__(self, token: JNToken, vocabs: VocabCollection) -> None:
        super().__init__(token.surface, token.base_form, token.base_form)
        self.token = token
        self._vocabs = vocabs
        self.is_inflectable_word = self.token.is_inflectable_word()

    def pre_process(self) -> list[ProcessedToken]:
        vocab_based_potential_verb_split = self._try_find_vocab_based_potential_verb_compound()
        if vocab_based_potential_verb_split: return vocab_based_potential_verb_split

        dictionary_based_potential_verb_split = self._try_find_dictionary_based_potential_verb_compound()
        if dictionary_based_potential_verb_split: return dictionary_based_potential_verb_split

        return [self]

    def _try_find_vocab_based_potential_verb_compound(self) -> list[ProcessedToken]:
        for vocab in self._vocabs.with_question(self.base_form):
            compound_parts = vocab.get_user_compounds()
            if len(compound_parts) == 2 and compound_parts[1] == "える":
                return self._build_potential_verb_compound(compound_parts[0])
        return []

    def _try_find_dictionary_based_potential_verb_compound(self) -> list[ProcessedToken]:
        if (len(self.token.base_form) >= 3
                and self.token.base_form[-2:] in conjugator.godan_potential_verb_ending_to_dictionary_form_endings
                and self.token.is_verb()):
            if not DictLookup.is_word(self.token.base_form): #the potential verbs are generally not in the dictionary this is how we know them
                root_verb = conjugator.construct_root_verb_for_possibly_potential_godan_verb_dictionary_form(self.token.base_form)
                if DictLookup.is_word(root_verb):
                    lookup = DictLookup.lookup_word_shallow(root_verb)
                    if lookup.found_words():
                        is_godan = any(e for e in lookup.entries if "godan verb" in e.parts_of_speech())
                        if not is_godan:
                            return []
                    return self._build_potential_verb_compound(root_verb)
        return []

    def _build_potential_verb_compound(self, root_verb: str) -> list[ProcessedToken]:
        root_verb_e_stem = conjugator.get_e_stem(root_verb, is_godan=True)
        root_verb_eru_stem = root_verb_e_stem[:-1]
        potential_stem_ending = root_verb_e_stem[-1]
        root_verb_token = SplitToken(root_verb_eru_stem, root_verb, root_verb, True, True)
        final_character = "る" if self.surface[-1] == "る" else ""
        eru_token = SplitToken(f"{potential_stem_ending}{final_character}", f"{potential_stem_ending}る", "える", True, True)
        new_surface = root_verb_token.surface + eru_token.surface
        if new_surface != self.surface:
            log.warning(f"combined surface should be {self.surface} but is {new_surface}, bailing out")
            return []
        new_base = root_verb_token.surface + eru_token.base_form
        if new_base != self.base_form:
            log.warning(f"combined base should be {self.base_form} but is {new_base} bailing out")
            return []
        return [root_verb_token, eru_token]

class JNTokenizedText:
    def __init__(self, text: str, tokens: list[JNToken]) -> None:
        self.text = text
        self.tokens = tokens

    def pre_process(self) -> list[ProcessedToken]:
        from ankiutils import app
        vocab = app.col().vocab

        step1 = [JNTokenWrapper(token, vocab) for token in self.tokens]
        step2 = ex_sequence.flatten([token.pre_process() for token in step1])

        return step2
