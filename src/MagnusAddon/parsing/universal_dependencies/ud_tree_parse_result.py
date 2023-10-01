from typing import Callable

from parsing.universal_dependencies.ud_tree_node import UDTreeNode


class UDTreeParseResult:
    def __init__(self, *args: UDTreeNode) -> None:
        self.nodes = list(args)

    def __repr__(self) -> str:
        _argument_separator = ",\n"
        return f"""R(\n{_argument_separator.join(repr(node) for node in self.nodes)})"""

    def __str__(self) -> str:
        _argument_separator = "\n"
        return f"""{_argument_separator.join(str(node) for node in self.nodes)}"""

    def __eq__(self, other) -> bool:
        return (isinstance(other, UDTreeParseResult)
                and self.nodes == other.nodes)

    def visit(self, callback: Callable[['UDTreeNode'], None]) -> None:
        for node in self.nodes:
            node.visit(callback)