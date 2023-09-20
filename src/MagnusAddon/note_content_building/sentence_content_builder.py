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
        vocabs = WaniCollection.search_vocab_notes(search_utils.node_vocab_lookup(node))

        if vocabs:
            for vocab in vocabs:
                html += f"""
<li>
    <span class="vocabQuestion clipboard">{vocab.get_question()}</span>
    <span class="vocabAnswer">{vocab.get_active_answer()}</span>
    {create_html_from_nodes(node.children)}
</li>
"""
        else:
            html += f"""
<li>
    <span class="vocabQuestion clipboard">{node.base}</span>
    <span class="vocabAnswer">NO VOCAB FOUND</span>
    {create_html_from_nodes(node.children)}
</li>
"""


    html += "</ul>\n"

    return html

def build_breakdown_html(sentence: SentenceNote) -> None:
    user_excluded = sentence.get_user_excluded_vocab()
    excluded = user_excluded | _ignored_vocab

    question = sentence.get_active_question()
    nodes = tree_parser.parse_tree(question, user_excluded)

    html = create_html_from_nodes(nodes)
    sentence.set_break_down(html)
