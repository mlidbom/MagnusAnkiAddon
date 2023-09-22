from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.parts_of_speech import POS
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from parsing.tree_parsing.parse_tree_node import Node
from sysutils import kana_utils
from sysutils.utils import ListUtils

_tokenizer = TokenizerExt()

_max_lookahead = 12

def parse_tree(sentence:str, excluded:set[str]) -> list[Node]:
    tokens = _tokenizer.tokenize(sentence).tokens
    if not tokens:
        return []
    if _is_in_dictionary(tokens, excluded):
        return [Node.create(tokens, excluded)]
    
    dictionary_compounds_added = _build_dictionary_compounds(tokens, excluded)
    verb_compounds_added = _build_verb_compounds(dictionary_compounds_added, excluded)
    return [Node.create(compounds, excluded) for compounds in verb_compounds_added]


def _internal_parse(tokens: list[TokenExt], excluded:set[str]) -> list[Node]:
    dictionary_compounds = _build_dictionary_compounds(tokens, excluded)
    return [Node.create(compounds, excluded) for compounds in dictionary_compounds]

def _build_verb_compounds(start_compounds: list[list[TokenExt]], excluded:set[str]) -> list[list[TokenExt]]:
    compounds = start_compounds
    verb_compound_index = 0
    compound_count = len(compounds)
    while verb_compound_index < compound_count:
        verb_compound = compounds[verb_compound_index]
        if len(verb_compound) > 0:
            candidate_verb = verb_compound[-1]
            if candidate_verb.is_verb():
                auxiliary_index = verb_compound_index + 1
                while auxiliary_index < compound_count:
                    candidate_auxiliary_compound = compounds[auxiliary_index]
                    candidate_auxiliary_compound_copy = [v for v in candidate_auxiliary_compound]

                    found_auxiliaries:list[int] = []
                    for candidate_index, cand in enumerate(candidate_auxiliary_compound_copy):
                        if not cand.is_verb_auxiliary():
                            break
                        verb_compound.append(cand)
                        found_auxiliaries.append(candidate_index)

                    if len(found_auxiliaries) == 0:
                        break

                    found_auxiliaries.reverse()
                    for found in found_auxiliaries:
                        candidate_auxiliary_compound.pop(found)

                    if len(candidate_auxiliary_compound) > 0:
                        break

                    auxiliary_index += 1
        verb_compound_index += 1

    result_compounds = [comp for comp in compounds if len(comp) > 0]
    return result_compounds

def _is_in_dictionary(compound_tokens: list[TokenExt], excluded:set[str]) -> bool:
    compound_surface = "".join([tok.surface for tok in compound_tokens])
    compound_base = "".join([tok.surface for tok in compound_tokens[:-1]]) + compound_tokens[-1].base_form

    if compound_base in excluded: return False

    return (DictLookup.lookup_word_shallow(compound_base).found_words()
            or DictLookup.lookup_word_shallow(compound_surface).found_words())


def _build_dictionary_compounds(tokens: list[TokenExt], excluded:set[str]) -> list[list[TokenExt]]:
    compounds: list[list[TokenExt]] = []

    identity_index = len(tokens)
    while len(tokens) > 0:
        max_lookahead = min(_max_lookahead, len(tokens))
        current_index = max_lookahead
        while current_index > 0:
            compound_tokens = tokens[:current_index]
            if current_index != identity_index and _is_in_dictionary(compound_tokens, excluded):
                compounds.append(compound_tokens)
                tokens = tokens[current_index:]
                break

            current_index -= 1

        if current_index == 0:
            if tokens[0].base_form not in excluded and tokens[0].surface not in excluded:
                compounds.append([tokens[0]])
            tokens = tokens[1:]

    return compounds

def _find_compounds(token: TokenExt, excluded:set[str]) -> list[Node]:
    for index, character in enumerate(token.base_form):
        part_1 = token.base_form[:index]
        part_2 = token.base_form[index:]
        if (part_1
                and part_2
                and not kana_utils.is_only_kana(part_1)
                and not kana_utils.is_only_kana(part_2)):
            tokens_1 = _tokenizer.tokenize(part_1)
            if tokens_1.tokens and _is_in_dictionary(tokens_1.tokens, excluded):
                tokens_2 = _tokenizer.tokenize(part_2)
                if tokens_2.tokens and _is_in_dictionary(tokens_2.tokens, excluded):
                    return [Node.create_non_recursive(tokens_1.tokens), Node.create_non_recursive(tokens_2.tokens)]


    return []