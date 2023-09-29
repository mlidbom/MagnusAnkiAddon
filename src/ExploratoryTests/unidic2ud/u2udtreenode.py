from parsing.janome_extensions.token_ext import TokenExt

class U2UdTreeNode:
    _max_lookahead = 12

    def __init__(self, surface: str, base: str, children: list['U2UdTreeNode'] = None, tokens: list[TokenExt] = None) -> None:
        self.surface = surface
        self.base = base if base else surface
        self.tokens = tokens
        self.children: list[U2UdTreeNode] = children if children else []

    def _children_repr(self, level=1) -> str:
        if not self.children:
            return ""
        indent = "  " * level
        children_string = ', '.join(child._repr(level) for child in self.children)
        return f""",[\n{indent}{children_string}]"""

    def _repr(self, level: int):
        return f"""N('{self.surface}', '{self.base if self.is_inflected() else ""}'{self._children_repr(level + 1)})"""

    def __repr__(self) -> str:
        return self._repr(0)

    def __eq__(self, other: any) -> bool:
        return (isinstance(other, U2UdTreeNode)
                and self.base == other.base
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)

    def is_inflected(self) -> bool:
        return self.base != self.surface

    @classmethod
    def create(cls, tokens: list[TokenExt], excluded: set[str]) -> 'U2UdTreeNode':
        children = tree_parser._recursing_parse(tokens, excluded) if len(tokens) > 1 else []  # tree_parser._find_compounds(tokens[0], excluded) # noqa
        return cls.create_non_recursive(tokens, children)

    @classmethod
    def create_non_recursive(cls, tokens: list[TokenExt], children: list['U2UdTreeNode'] = None) -> 'U2UdTreeNode':
        children = children if children else []
        surface = "".join(tok.surface for tok in tokens)
        base = "".join(tok.surface for tok in tokens[:-1]) + tokens[-1].base_form
        return U2UdTreeNode(surface, base, children, tokens)
