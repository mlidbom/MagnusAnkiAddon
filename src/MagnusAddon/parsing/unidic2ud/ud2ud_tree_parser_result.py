from typing import Callable

from parsing.unidic2ud.ud2ud_tree_node import UD2UDTreeNode


class UD2UDParseResult:
    def __init__(self, *args: UD2UDTreeNode) -> None:
        self.nodes = list(args)

    def __repr__(self) -> str:
        _argument_separator = ",\n  "
        return f"""R({_argument_separator.join(node._repr(1) for node in self.nodes)})""" # noqa

    def __str__(self) -> str:
        _argument_separator = "\n"
        return f"""{_argument_separator.join(node._str(0) for node in self.nodes)}""" # noqa

    def __eq__(self, other) -> bool:
        return (isinstance(other, UD2UDParseResult)
                and self.nodes == other.nodes)

    def visit(self, callback: Callable[['UD2UDTreeNode'], None]) -> None:
        for node in self.nodes:
            node.visit(callback)