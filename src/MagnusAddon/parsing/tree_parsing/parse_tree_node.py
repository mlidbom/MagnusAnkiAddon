from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.token_ext import TokenExt
from parsing.tree_parsing import tree_parser


class Node:
    _max_lookahead = 12
    def __init__(self, surface: str, children=None) -> None:
        self.surface = surface
        self.children = children if children else []

    def __repr__(self) -> str:
        return f"""Node('{self.surface}'{"," + str(self.children) if self.children else ""})"""

    def __eq__(self, other: any) -> bool:
        return (isinstance(other, Node)
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)

    @classmethod
    def create(cls, tokens: list[TokenExt]) -> 'Node':
        children = tree_parser.internal_parse(tokens) if len(tokens) > 1 else None
        surface = "".join(tok.surface for tok in tokens)
        return Node(surface, children)