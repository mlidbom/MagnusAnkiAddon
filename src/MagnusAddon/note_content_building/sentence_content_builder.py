from ankiutils import search_utils
from note.sentencenote import SentenceNote
from note.wanivocabnote import WaniVocabNote
from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.parse_tree_node import Node
from sysutils.utils import StringUtils, ListUtils
from wanikani.wani_collection import WaniCollection

_ignored_tokens: set[str] = set("しもよかとたてでをなのにだがは")
_ignored_vocab: set[str] = {"擦る"}

def create_html_from_nodes(nodes: list[Node], excluded: set[str], depth:int) -> str:
    html = f"""<ul class="sentenceVocabList depth{depth}">\n"""

    for node in nodes:
        if node.surface in excluded or node.base in excluded:
            continue

        vocabs = WaniCollection.search_vocab_notes(search_utils.node_vocab_lookup(node))
        vocabs = [voc for voc in vocabs if voc.get_question() not in excluded]

        found_words = set((voc.get_question() for voc in vocabs)) | set(ListUtils.flatten_list([voc.get_readings() for voc in vocabs]))

        if vocabs:
            for vocab in vocabs:
                html += f"""
<li class="sentenceVocabEntry depth{depth}">
    <span class="vocabQuestion clipboard">{vocab.get_display_question()}</span>
    <span class="vocabAnswer">{vocab.get_active_answer()}</span>
    {create_html_from_nodes(node.children, excluded, depth + 1)}
</li>
"""
            if node.surface and node.is_surface_dictionary_word() and node.surface not in found_words:
                html += f"""
<li class="sentenceVocabEntry depth{depth}">
    <span class="vocabQuestion clipboard">{node.surface}</span>
    <span class="vocabAnswer">-</span>
    {create_html_from_nodes(node.children, excluded, depth + 1)}
</li>
"""

        else:
            html += f"""
<li class="sentenceVocabEntry depth{depth}">
    <span class="vocabQuestion clipboard">{node.base}</span>
    <span class="vocabAnswer">-</span>
    {create_html_from_nodes(node.children, excluded, depth + 1)}
</li>
"""
            if node.is_surface_dictionary_word():
                html += f"""
<li class="sentenceVocabEntry depth{depth}">
    <span class="vocabQuestion clipboard">{node.surface}</span>
    <span class="vocabAnswer">-</span>
    {create_html_from_nodes(node.children, excluded, depth + 1)}
</li>
"""




    html += "</ul>\n"

    return html

def build_breakdown_html(sentence: SentenceNote) -> None:
    user_excluded = sentence.get_user_excluded_vocab()
    excluded = user_excluded | _ignored_vocab

    question = sentence.get_active_question()
    nodes = tree_parser.parse_tree(question, user_excluded)

    html = create_html_from_nodes(nodes, excluded, 1)
    sentence.set_break_down(html)
