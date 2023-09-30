from typing import Callable

from parsing.unidic2ud.u2udtreenode import U2UdTreeNode


class U2UdParseResult:
    def __init__(self, *args: U2UdTreeNode) -> None:
        self.nodes = list(args)

    def __repr__(self) -> str:
        _argument_separator = ",\n  "
        return f"""R({_argument_separator.join(node._repr(1) for node in self.nodes)})""" # noqa

    def __str__(self) -> str:
        _argument_separator = "\n"
        return f"""{_argument_separator.join(node._str(0) for node in self.nodes)}""" # noqa

    def __eq__(self, other) -> bool:
        return (isinstance(other, U2UdParseResult)
                and self.nodes == other.nodes)

    def visit(self, callback: Callable[['U2UdTreeNode'], None]) -> None:
        for node in self.nodes:
            node.visit(callback)