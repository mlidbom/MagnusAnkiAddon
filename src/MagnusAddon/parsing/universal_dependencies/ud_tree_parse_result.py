from typing import Callable, Any

from parsing.universal_dependencies.ud_tree_node import UDTextTreeNode


class UDTextTree:
    def __init__(self, *args: UDTextTreeNode) -> None:
        self.nodes = list(args)

    def __repr__(self) -> str:
        _argument_separator = ",\n"
        return f"""R(\n{_argument_separator.join(repr(node) for node in self.nodes)})"""

    def __str__(self) -> str:
        _argument_separator = "\n"
        return f"""{_argument_separator.join(str(node) for node in self.nodes)}"""

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, UDTextTree)
                and self.nodes == other.nodes)

    def visit(self, callback: Callable[['UDTextTreeNode'], None]) -> None:
        for node in self.nodes:
            node.visit(callback)