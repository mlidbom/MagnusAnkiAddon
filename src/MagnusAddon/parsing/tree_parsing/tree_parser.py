from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from parsing.tree_parsing.parse_tree_node import Node

_tokenizer = TokenizerExt()

def build_tree(sentence: str) -> Node:
    tokens = _tokenizer.tokenize(sentence).tokens
    return Node.create(tokens, set())


_max_lookahead = 12


def temp_test_method(sentence: str) -> list[list[TokenExt]]:
    tokens = _tokenizer.tokenize(sentence).tokens
    return list_compounds(tokens, set())

def parse_tree(sentence:str, excluded:set[str]) -> list[Node]:
    tokens = _tokenizer.tokenize(sentence).tokens
    if _is_in_dictionary(tokens, set()): return [Node.create(tokens, excluded)]
    return internal_parse(tokens, excluded)


def internal_parse(tokens, excluded:set[str]) -> list[Node]:
    return [Node.create(tokens, excluded) for tokens in list_compounds(tokens, excluded)]

def _is_in_dictionary(compound_tokens: list[TokenExt], excluded:set[str]) -> bool:
    compound_surface = "".join([tok.surface for tok in compound_tokens])
    compound_base = "".join([tok.surface for tok in compound_tokens[:-1]]) + compound_tokens[-1].base_form

    if compound_base in excluded or compound_surface in excluded: return False

    return (DictLookup.lookup_word_shallow(compound_surface).found_words()
            or DictLookup.lookup_word_shallow(compound_base).found_words())

def _is_excluded(compound_tokens: list[TokenExt], excluded:set[str]):
    compound_surface = "".join([tok.surface for tok in compound_tokens])
    compound_base = "".join([tok.surface for tok in compound_tokens[:-1]]) + compound_tokens[-1].base_form
    return compound_base in excluded or compound_surface in excluded


def list_compounds(tokens: list[TokenExt], excluded:set[str]) -> list[list[TokenExt]]:
    compounds: list[list[TokenExt]] = []

    current_index = 1
    while len(tokens) > 0:
        max_lookahead = min(_max_lookahead, len(tokens)) - 1
        current_index = max_lookahead
        while current_index > 0:
            compound_tokens = tokens[:current_index]
            if _is_in_dictionary(compound_tokens, excluded):
                compounds.append(compound_tokens)
                tokens = tokens[current_index:]
                break

            current_index -= 1

        if current_index == 0:
            if tokens[0].base_form not in excluded and tokens[0].surface not in excluded:
                compounds.append([tokens[0]])
            tokens = tokens[1:]

    return compounds