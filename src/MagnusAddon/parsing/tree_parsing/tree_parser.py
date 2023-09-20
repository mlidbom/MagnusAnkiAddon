from typing import List

from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from parsing.tree_parsing.parse_tree_node import Node

_tokenizer = TokenizerExt()

def build_tree(sentence: str) -> Node:
    tokens = _tokenizer.tokenize(sentence).tokens
    return Node.create(tokens)


_max_lookahead = 12


def temp_test_method(sentence: str) -> list[list[TokenExt]]:
    tokens = _tokenizer.tokenize(sentence).tokens
    return list_compounds(tokens)

def parse_tree(sentence:str) -> list[Node]:
    tokens = _tokenizer.tokenize(sentence).tokens
    if _is_in_dictionary(tokens): return [Node.create(tokens)]
    return internal_parse(tokens)


def internal_parse(tokens) -> list[Node]:
    return [Node.create(tokens) for tokens in list_compounds(tokens)]


def _is_in_dictionary(compound_tokens: list[TokenExt]) -> bool:
    compound_root = "".join([tok.surface for tok in compound_tokens])
    compound_base = "".join([tok.surface for tok in compound_tokens[:-1]]) + compound_tokens[-1].base_form
    return (DictLookup.lookup_word_shallow(compound_root).found_words()
            or DictLookup.lookup_word_shallow(compound_base).found_words())


def list_compounds(tokens: list[TokenExt]) -> list[list[TokenExt]]:
    compounds: list[list[TokenExt]] = []

    current_index = 1
    while current_index > 0:
        max_lookahead = min(_max_lookahead, len(tokens)) - 1
        current_index = max_lookahead
        while current_index > 0:
            compound_tokens = tokens[:current_index]
            if _is_in_dictionary(compound_tokens):
                compounds.append(compound_tokens)
                tokens = tokens[current_index:]
                break

            current_index -= 1

        if current_index == 0:
            compounds.append([tokens[0]])

    return compounds