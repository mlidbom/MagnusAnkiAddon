from note.sentencenote import SentenceNote
from parsing.universal_dependencies import ud_parsers, ud_tree_parser
from parsing.universal_dependencies.ud_tree_node import UDTreeNode
from parsing.universal_dependencies.ud_tree_parse_result import UDTreeParseResult
from sysutils.stringutils import StringUtils


class NodeViewModel:
    def __init__(self, node: UDTreeNode):
        self._node = node
        self.children = [NodeViewModel(nod) for nod in node.children]

    def str_(self, depth:int) -> str:
        padding = "  " * depth
        return f"""{padding}{self._node.surface} : {self._node.base if self._node.is_inflected() else ""} {self.str_children(depth)}"""

    def str_children(self, depth:int) -> str:
        if not self.children: return ""

        return f"""\n{StringUtils.newline().join([m.str_(depth + 1) for m in self.children])} """


class BreakDownViewModel:
    def __init__(self, parse_result: UDTreeParseResult):
        self._parse_result = parse_result
        self.nodes = [NodeViewModel(node) for node in parse_result.nodes]

    def __str__(self) -> str:
        return "\n".join([m.str_(0) for m in self.nodes])

def create(sentence: SentenceNote):
    question = sentence.get_active_question()
    parse_result = ud_tree_parser.parse(ud_parsers.best, question)

    return BreakDownViewModel(parse_result)

