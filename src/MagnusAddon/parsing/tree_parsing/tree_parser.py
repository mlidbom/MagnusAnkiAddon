from typing import Callable

from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from parsing.tree_parsing.node import Node

_tokenizer = TokenizerExt()

_max_lookahead = 12

def parse_tree_ui(sentence:str, excluded:set[str]) -> list[Node]:
    nodes = parse_tree(sentence, excluded)
    if len(nodes) == 1:
        node = nodes[0]
        if node.base and DictLookup.lookup_word_shallow(node.base).found_words() or node.surface and DictLookup.lookup_word_shallow(node.surface).found_words():
            return nodes
        else:
            return node.children
    return nodes

def parse_tree(sentence:str, excluded:set[str]) -> list[Node]:
    tokens = _tokenizer.tokenize(sentence).tokens
    if not tokens:
        return []
    if _is_in_dictionary(tokens, excluded):
        return [Node.create(tokens, excluded)]
    
    dictionary_compounds_added = _build_dictionary_compounds(tokens, excluded)
    verb_compounds_added = _build_compounds(is_verb, is_verb_auxiliary, dictionary_compounds_added, excluded)
    adjective_compounds_added = _build_compounds(_is_adjective, _is_adjective_auxiliary, verb_compounds_added, excluded)
    noun_compounds_added = _build_compounds(_is_noun, _is_noun_auxiliary, adjective_compounds_added, excluded)
    return [Node.create(compounds, excluded) for compounds in noun_compounds_added]


def _recursing_parse(tokens, excluded:set[str]) -> list[Node]:
    dictionary_compounds = _build_dictionary_compounds(tokens, excluded)
    adjective_compounds_added = _build_compounds(_is_adjective, _is_adjective_auxiliary, dictionary_compounds, excluded)
    if len(adjective_compounds_added) > 1:
        if len(adjective_compounds_added) != len(dictionary_compounds):
            return [Node.create(compounds, excluded) for compounds in adjective_compounds_added]

    verb_compounds_added = _build_compounds(is_verb, is_verb_auxiliary, dictionary_compounds, excluded)
    if len(verb_compounds_added) > 1:
        if len(verb_compounds_added) != len(dictionary_compounds):
            return [Node.create(compounds, excluded) for compounds in verb_compounds_added]

    return [Node.create(compounds, excluded) for compounds in dictionary_compounds]

def is_verb(compound: list[TokenExt]):
    return compound[-1].is_verb()

def _is_adjective(compound: list[TokenExt]):
    return compound[-1].is_adjective()

def _is_noun(compound: list[TokenExt]):
    return compound[-1].is_noun()

def is_verb_auxiliary(compound: list[TokenExt]):
    return compound[0].is_verb_auxiliary()

def _is_adjective_auxiliary(compound: list[TokenExt]):
    return all(c.is_adjective_auxiliary() for c in compound)

def _is_noun_auxiliary(compound: list[TokenExt]):
    return all(c.is_noun_auxiliary() for c in compound)

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

def _is_excluded(compound_tokens: list[TokenExt], excluded:set[str]) -> bool:
    compound_base = "".join([tok.surface for tok in compound_tokens[:-1]]) + compound_tokens[-1].base_form
    return compound_base in excluded

def _is_in_dictionary(compound_tokens: list[TokenExt], excluded:set[str]) -> bool:
    compound_surface = "".join([tok.surface for tok in compound_tokens])
    compound_base = "".join([tok.surface for tok in compound_tokens[:-1]]) + compound_tokens[-1].base_form

    if compound_base in excluded: return False

    return (DictLookup.lookup_word_shallow(compound_base).found_words()
            or DictLookup.lookup_word_shallow(compound_surface).found_words())


def _build_dictionary_compounds(tokens_param: list[TokenExt], excluded:set[str]) -> list[list[TokenExt]]:
    compounds: list[list[TokenExt]] = []
    tokens = [tok for tok in tokens_param]

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
            left_over_token = tokens[0]
            if left_over_token.base_form in excluded or left_over_token.surface in excluded:
                # we are in bad shape here. We don't want to exclude single tokens or a part of the sentence just disappears for the user. Most likely the tokenizer has made a mistake that the user is trying to correct by excluding the word. So let's see if we can jiggle the tokenizer to make a choice the user likes better.
                if len(left_over_token.surface) == 1: # for whatever reason the user does not want to display this single character as a separate word. That's fine, but we handle that on the UI level by excluding it there, here we want it preserved for the verb and adjective compound logic to make use of.
                    compounds.append([left_over_token])
                elif len(left_over_token.surface) > 1: # Try and see what happens if we just give this tiny thing to the tokenizer, it ain't pretty but we're desperate here.
                    tokenized_text = _tokenizer.tokenize(left_over_token.surface)
                    if len(tokenized_text.tokens) > 1:
                        for token in tokenized_text.tokens:
                            compounds.append([token])# Try and see what happens if we just give this tiny thing to the tokenizer, it ain't pretty but we're desperate
                    else: # OK. Now we are at the very bottom of the barrel. We'll just split it manually and give the parts to the tokenizer. Hold your nose and squeeze your eyes shut. This is some truly ugly code.
                        characters = list(left_over_token.surface)
                        tokenized_single_characters = [_tokenizer.tokenize(char).tokens for char in characters]
                        if not all(len(c) == 1 for c in tokenized_single_characters): raise Exception("Somehow a single character resulted in i multi token result??")
                        compounds.extend(tokenized_single_characters)
            else:
                compounds.append([tokens[0]])

            tokens = tokens[1:]

    return compounds