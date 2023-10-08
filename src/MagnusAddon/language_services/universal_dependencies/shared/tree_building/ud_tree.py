from typing import Callable, Any

from language_services.universal_dependencies.shared.tree_building.ud_tree_node import UDTreeNode


class UDTree:
    def __init__(self, *args: UDTreeNode) -> None:
        self.nodes = list(args)

    def __repr__(self) -> str:
        _argument_separator = ",\n"
        return f"""R(\n{_argument_separator.join(repr(node) for node in self.nodes)})"""

    def __str__(self) -> str:
        _argument_separator = "\n"
        return f"""{_argument_separator.join(str(node) for node in self.nodes)}"""

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, UDTree)
                and self.nodes == other.nodes)

    def visit(self, callback: Callable[['UDTreeNode'], None]) -> None:
        for node in self.nodes:
            node.visit(callback)

    def flatten(self) -> list[UDTreeNode]:
        nodes:list[UDTreeNode] = []
        def add_node(node: UDTreeNode) -> None:
            nodes.append(node)

        self.visit(add_node)
        return nodes