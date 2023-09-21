from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.token_ext import TokenExt
from parsing.tree_parsing import tree_parser
from sysutils import kana_utils


class Node:
    _max_lookahead = 12
    def __init__(self, base: str, surface: str, children=None, tokens: list[TokenExt] = None) -> None:
        self.base = base
        self.surface = surface
        self.tokens = tokens
        self.children = children if children else []

    def __repr__(self) -> str:
        return f"""Node('{self.base}','{self.surface}'{"," + str(self.children) if self.children else ""})"""

    def __eq__(self, other: any) -> bool:
        return (isinstance(other, Node)
                and self.base == other.base
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)

    @classmethod
    def create(cls, tokens: list[TokenExt], excluded:set[str]) -> 'Node':
        children = tree_parser._internal_parse(tokens, excluded) if len(tokens) > 1 else None # noqa
        surface = "".join(tok.surface for tok in tokens)
        base = "".join(tok.surface for tok in tokens[:-1]) + tokens[-1].base_form
        surface = surface if base != surface else ""
        return Node(base, surface, children, tokens)

    def is_base_kana_only(self) -> bool:
        return kana_utils.is_only_kana(self.base)

    def is_surface_kana_only(self) -> bool:
        return self.surface and kana_utils.is_only_kana(self.surface)

    def is_surface_dictionary_word(self) -> bool:
        return self.surface and DictLookup.lookup_word_shallow(self.surface).found_words()