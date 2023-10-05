from note.collection.jp_collection import JPCollection
from note.sentencenote import SentenceNote
from parsing.universal_dependencies import ud_parsers, ud_tree_builder
from parsing.universal_dependencies.ud_tree_node import UDTextTreeNode
from parsing.universal_dependencies.ud_tree_parse_result import UDTextTree

class NodeViewModel:
    def __init__(self, node: UDTextTreeNode, collection: JPCollection):
        self._node = node
        self._collection = collection
        self.children = [NodeViewModel(nod, collection) for nod in node.children]


    def surface(self) -> str: return self._node.surface
    def base(self) -> str: return self._node.base if self._node.base != self._node.surface else ""


class BreakDownViewModel:
    def __init__(self, parse_result: UDTextTree, collection: JPCollection):
        self._parse_result = parse_result
        self.nodes = [NodeViewModel(node, collection) for node in parse_result.nodes]

def create(sentence: SentenceNote, collection: JPCollection) -> BreakDownViewModel:
    question = sentence.get_question()
    parse_result = ud_tree_builder.build_tree(ud_parsers.best, question)

    return BreakDownViewModel(parse_result, collection)

