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
    return internal_parse(tokens)


def internal_parse(tokens) -> list[Node]:
    return [Node.create(tokens) for tokens in list_compounds(tokens)]


def list_compounds(tokens: list[TokenExt]) -> list[list[TokenExt]]:
    compounds: list[list[TokenExt]] = []

    current_index = 1
    while current_index > 0:
        max_lookahead = min(_max_lookahead, len(tokens)) - 1
        current_index = max_lookahead
        while current_index > 0:
            compound_tokens = [tok for tok in tokens[:current_index]]
            compound_root = "".join([tok.surface for tok in compound_tokens])
            if DictLookup.lookup_word_shallow(compound_root).found_words():
                compounds.append(compound_tokens)
                tokens = tokens[current_index:]
                break

            current_index -= 1

        if current_index == 0:
            compounds.append([tokens[0]])

    return compounds