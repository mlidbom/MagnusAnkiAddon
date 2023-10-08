from __future__ import annotations

from typing import Any
from language_services.universal_dependencies.shared.tree_building.ud_tree import UDTree
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_node_spec import UDTreeNodeSpec

class UDTreeSpec:
    def __init__(self, *args: UDTreeNodeSpec) -> None:
        self.nodes = list(args)

    def __repr__(self) -> str:
        _argument_separator = ",\n"
        return f"""R(\n{_argument_separator.join(repr(node) for node in self.nodes)})"""

    def __str__(self) -> str:
        _argument_separator = "\n"
        return f"""{_argument_separator.join(str(node) for node in self.nodes)}"""

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, UDTreeSpec)
                and self.nodes == other.nodes)

    def clone_level_0_to_level_1(self) -> UDTreeSpec:
        cloned_nodes = [node.clone_as_level(0) for node in self.nodes]
        for node in cloned_nodes:
            node.children.append(node.clone_as_level(1))
        return UDTreeSpec(*cloned_nodes)

    @staticmethod
    def from_ud_tree(tree: UDTree, max_depth:int = 99) -> UDTreeSpec:
        return UDTreeSpec(*[UDTreeNodeSpec.from_node(node, max_depth) for node in tree.nodes])
