from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.parts_of_speech import POS
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from parsing.tree_parsing.parse_tree_node import Node

_tokenizer = TokenizerExt()

_max_lookahead = 12

def parse_tree(sentence:str, excluded:set[str]) -> list[Node]:
    tokens = _tokenizer.tokenize(sentence).tokens
    if _is_in_dictionary(tokens, excluded): return [Node.create(tokens, excluded)]
    stage1 = _list_compounds(tokens, excluded)
    stage2 = _restore_verb_forms(stage1, excluded)
    return [Node.create(compounds, excluded) for compounds in stage2]


def _internal_parse(tokens, excluded:set[str]) -> list[Node]:
    stage1 = _list_compounds(tokens, excluded)
    return [Node.create(compounds, excluded) for compounds in stage1]

def _restore_verb_forms(start_compounds: list[list[TokenExt]], excluded:set[str]) -> list[list[TokenExt]]:
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


def _list_compounds(tokens: list[TokenExt], excluded:set[str]) -> list[list[TokenExt]]:
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