from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from parsing.tree_parsing.tree_parser_node import TreeParserNode

class TreeParseResult:
    def __init__(self, *args: TreeParserNode) -> None:
        self.nodes = list(args)

    def __repr__(self) -> str:
        _argument_separator = ",\n  "
        return f"""R({_argument_separator.join(node._repr(1) for node in self.nodes)})""" # noqa

    def __eq__(self, other:Any) -> bool:
        return (isinstance(other, TreeParseResult)
                and self.nodes == other.nodes)

    def visit(self, callback: Callable[[TreeParserNode], None]) -> None:
        for node in self.nodes:
            node.visit(callback)