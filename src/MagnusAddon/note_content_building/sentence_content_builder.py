from ankiutils import search_utils
from note.sentencenote import SentenceNote
from note.wanivocabnote import WaniVocabNote
from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.parse_tree_node import Node
from sysutils.utils import StringUtils, ListUtils
from wanikani.wani_collection import WaniCollection

_ignored_tokens: set[str] = set("しもよかとたてでをなのにだがは")
_ignored_vocab: set[str] = {"擦る"}

def vocab_html(node: Node, excluded:set[str], question:str, answer:str, depth:int) -> str:
    html = f"""
    <li class="sentenceVocabEntry depth{depth}">
        <span class="vocabQuestion clipboard">{question}</span>
        <span class="vocabAnswer">{answer}</span>
        {create_html_from_nodes(node.children, excluded, depth + 1)}
    </li>
    """

    return html

def create_html_from_nodes(nodes: list[Node], excluded: set[str], depth:int) -> str:
    html = f"""<ul class="sentenceVocabList depth{depth}">\n"""

    for node in nodes:
        vocabs = WaniCollection.search_vocab_notes(search_utils.node_vocab_lookup(node))
        vocabs = [voc for voc in vocabs if voc.get_display_question() not in excluded]

        found_words = set((voc.get_question() for voc in vocabs)) | set(ListUtils.flatten_list([voc.get_readings() for voc in vocabs]))

        if vocabs:
            for vocab in vocabs:
                html += vocab_html(node, excluded, vocab.get_display_question(), vocab.get_active_answer(), depth)

            if (node.surface
                    and node.surface not in found_words
                    and node.surface not in excluded
                    and node.is_show_surface_in_sentence_breakdown()):

                html += vocab_html(node, excluded, node.surface, "---", depth)

        else:
            text = "" if node.is_verb_compound_not_dictionary_word() else "---"
            html += vocab_html(node, excluded, node.get_sentence_display_text(), text, depth)
            if node.is_show_surface_in_sentence_breakdown() and node.surface not in excluded:
                html += vocab_html(node, excluded, node.surface, "-", depth)

    html += "</ul>\n"

    return html

def build_breakdown_html(sentence: SentenceNote) -> None:
    user_excluded = sentence.get_user_excluded_vocab()
    excluded = user_excluded | _ignored_vocab

    question = sentence.get_active_question()
    nodes = tree_parser.parse_tree(question, user_excluded)

    html = create_html_from_nodes(nodes, excluded, 1)
    sentence.set_break_down(html)
