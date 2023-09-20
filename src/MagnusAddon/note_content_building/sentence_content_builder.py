import io

from ankiutils import search_utils
from note.sentencenote import SentenceNote
from note.wanivocabnote import WaniVocabNote
from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.parse_tree_node import Node
from sysutils.utils import StringUtils, ListUtils
from wanikani.wani_collection import WaniCollection

_ignored_tokens: set[str] = set("しもよかとたてでをなのにだがは")
_ignored_vocab: set[str] = {"擦る"}

def create_html_from_nodes(nodes: list[Node]) -> str:
    html = "<ul>\n"

    for node in nodes:
        html += f"<li>Base: {node.base}, Surface: {node.surface}\n"
        if node.children:
            html += create_html_from_nodes(node.children)
        html += "</li>\n"

    html += "</ul>\n"

    return html

def build_breakdown_html(sentence: SentenceNote) -> None:
    user_excluded = sentence.get_user_excluded_vocab()
    excluded = user_excluded | _ignored_vocab

    question = sentence.get_active_question()
    nodes = tree_parser.parse_tree(question, user_excluded)

    html = create_html_from_nodes(nodes)
    sentence.set_break_down(html)








