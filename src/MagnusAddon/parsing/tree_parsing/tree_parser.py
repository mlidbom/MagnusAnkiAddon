from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt
from parsing.tree_parsing.parse_tree_node import Node

_tokenizer = TokenizerExt()

def build_tree(sentence: str) -> Node:
    tokens = _tokenizer.tokenize(sentence).tokens
    return Node.create(tokens, set())


_max_lookahead = 12


def parse_tree(sentence:str, excluded:set[str]) -> list[Node]:
    tokens = _tokenizer.tokenize(sentence).tokens
    if _is_in_dictionary(tokens, set()): return [Node.create(tokens, excluded)]
    return _internal_parse(tokens, excluded)


def _internal_parse(tokens, excluded:set[str]) -> list[Node]:
    stage1 = [Node.create(tokens, excluded) for tokens in _list_compounds(tokens, excluded)]

    return stage1

def _is_in_dictionary(compound_tokens: list[TokenExt], excluded:set[str]) -> bool:
    compound_surface = "".join([tok.surface for tok in compound_tokens])
    compound_base = "".join([tok.surface for tok in compound_tokens[:-1]]) + compound_tokens[-1].base_form

    if compound_base in excluded or compound_surface in excluded: return False

    return (DictLookup.lookup_word_shallow(compound_surface).found_words()
            or DictLookup.lookup_word_shallow(compound_base).found_words())


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