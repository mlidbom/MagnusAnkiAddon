from typing import Callable

from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from parsing.tree_parsing.node import Node

_tokenizer = TokenizerExt()

_max_lookahead = 12

def parse_tree(sentence:str, excluded:set[str]) -> list[Node]:
    tokens = _tokenizer.tokenize(sentence).tokens
    if not tokens:
        return []
    if _is_in_dictionary(tokens, excluded):
        return [Node.create(tokens, excluded)]
    
    dictionary_compounds_added = _build_dictionary_compounds(tokens, excluded)
    verb_compounds_added = _build_compounds(_is_verb, _is_verb_auxiliary, dictionary_compounds_added, excluded)
    adjective_compounds_added = _build_compounds(_is_adjective, _is_adjective_auxiliary, verb_compounds_added, excluded)
    return [Node.create(compounds, excluded) for compounds in adjective_compounds_added]


def _internal_parse(tokens, excluded:set[str]) -> list[Node]:
    dictionary_compounds = _build_dictionary_compounds(tokens, excluded)
    return [Node.create(compounds, excluded) for compounds in dictionary_compounds]

def _is_verb(compound: list[TokenExt]):
    return compound[-1].is_verb()

def _is_verb_auxiliary(compound: list[TokenExt]):
    return compound[0].is_verb_auxiliary()

def _is_adjective(compound: list[TokenExt]):
    return compound[-1].is_adjective()

def _is_adjective_auxiliary(compound: list[TokenExt]):
    return compound[0].is_adjective_auxiliary()

def _build_compounds(compound_filter: Callable[[list[TokenExt]],bool], auxiliary_filter: Callable[[list[TokenExt]],bool], start_compounds: list[list[TokenExt]], excluded:set[str]) -> list[list[TokenExt]]:
    compounds = [inner_list.copy() for inner_list in start_compounds]
    compound_index = 0
    compound_count = len(compounds)
    while compound_index < compound_count:
        compound = compounds[compound_index]
        if compound:
            if compound_filter(compound):
                auxiliary_index = compound_index + 1
                accepted_auxiliaries: list[TokenExt] = []
                while auxiliary_index < compound_count:
                    candidate_auxiliaries = compounds[auxiliary_index]
                    compound_surface_form = "".join((v.surface for v in compound))
                    accepted_auxiliaries_surface = "".join((v.surface for v in accepted_auxiliaries))

                    if not auxiliary_filter(candidate_auxiliaries):
                        break

                    candidate_surface = "".join((v.surface for v in candidate_auxiliaries))
                    candidate_compound_surface = compound_surface_form + accepted_auxiliaries_surface + candidate_surface

                    if candidate_compound_surface in excluded:
                        break

                    for cand in candidate_auxiliaries:
                        accepted_auxiliaries.append(cand)

                    auxiliary_index += 1

                if accepted_auxiliaries:
                    for cand in accepted_auxiliaries: compound.append(cand)
                    for index in range(compound_index + 1, auxiliary_index): compounds[index].clear()


        compound_index += 1

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