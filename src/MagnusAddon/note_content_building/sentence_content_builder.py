from ankiutils import search_utils
from note.sentencenote import SentenceNote
from note.wanivocabnote import WaniVocabNote
from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.node import Node, priorities
from sysutils.utils import ListUtils
from wanikani.wani_collection import WaniCollection

_vocab_missing_string = "---"

def _vocab_node_html(node: Node, excluded:set[str], question:str, answer:str, depth:int) -> str:
    if question in excluded:
        return ""

    priority_class = f"word_priority_{node.get_priority_class(question)}"

    html = f"""
    <li class="sentenceVocabEntry depth{depth} {priority_class}">
        <div class="sentenceVocabEntryDiv">
            <span class="vocabQuestion clipboard">{question}</span>
            <span class="vocabAnswer">{answer}</span>
        </div>
        {_create_html_from_nodes(node.children, excluded, depth + 1)}
    </li>
    """
    return html

def _create_html_from_nodes(nodes: list[Node], excluded: set[str], depth:int) -> str:
    if not nodes:
        return ""

    html = f"""<ul class="sentenceVocabList depth{depth}">\n"""

    for node in nodes:
        vocabs:list[WaniVocabNote] = []
        found_words: set[str] = set()
        if node.is_show_at_all_in_sentence_breakdown():
            vocabs = WaniCollection.search_vocab_notes(search_utils.node_vocab_lookup(node))
            vocabs = [voc for voc in vocabs if voc.get_display_question() not in excluded]
            found_words = set((voc.get_question() for voc in vocabs)) | set(ListUtils.flatten_list([voc.get_readings() for voc in vocabs]))

        if vocabs:
            for vocab in vocabs:
                html += _vocab_node_html(node, excluded, vocab.get_display_question(), vocab.get_active_answer(), depth)

            if (node.surface
                    and node.surface not in found_words
                    and node.surface not in excluded
                    and node.is_show_surface_in_sentence_breakdown()):

                html += _vocab_node_html(node, excluded, node.surface, _vocab_missing_string, depth)

        else:
            text = "" if node.is_probably_not_dictionary_word() else _vocab_missing_string
            display_text = node.surface if depth == 1 and node.surface and node.is_probably_not_dictionary_word() else node.base
            html += _vocab_node_html(node, excluded, display_text, text, depth)
            if node.is_show_surface_in_sentence_breakdown() and node.surface not in excluded:
                html += _vocab_node_html(node, excluded, node.surface, _vocab_missing_string, depth)

    html += "</ul>\n"

    return html



def _build_user_extra_list(extra_words: list[str], excluded:set[str]) -> str:
    html = f"""<ul class="sentenceVocabList depth1">\n"""
    for word in extra_words:
        vocabs = WaniCollection.search_vocab_notes(search_utils.single_vocab_by_form_exact(word))
        vocabs = [voc for voc in vocabs if voc.get_display_question() not in excluded]

        if vocabs:
            for vocab in vocabs:
                html += f"""
                    <li class="sentenceVocabEntry depth1 word_priority_{priorities.very_high}">
                        <div class="sentenceVocabEntryDiv">
                            <span class="vocabQuestion clipboard">{vocab.get_display_question()}</span>
                            <span class="vocabAnswer">{vocab.get_active_answer()}</span>
                        </div>
                    </li>
                    """
        else:
            html += f"""
                <li class="sentenceVocabEntry depth1">
                    <div class="sentenceVocabEntryDiv">
                        <span class="vocabQuestion clipboard">{word}</span>
                        <span class="vocabAnswer">{_vocab_missing_string}</span>
                    </div>
                </li>
                """

    html += "</ul>\n"
    return html


def build_breakdown_html(sentence: SentenceNote) -> None:
    user_excluded = sentence.get_user_excluded_vocab()
    extra_words = sentence.get_user_extra_vocab()
    html = ""
    if extra_words:
        html += _build_user_extra_list(extra_words, user_excluded)
        html += """\n<hr class="afterUserExtraWordsHR">\n"""

    question = sentence.get_active_question()
    nodes = tree_parser.parse_tree(question, user_excluded)

    html += _create_html_from_nodes(nodes, user_excluded, 1)
    sentence.set_break_down(html)
