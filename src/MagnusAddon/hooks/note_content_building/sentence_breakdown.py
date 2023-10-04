from anki.cards import Card
from aqt import gui_hooks

from ankiutils import search_utils
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.tree_parser_node import TreeParserNode, priorities
from sysutils.collections.recent_items import RecentItems
from ankiutils import app
from sysutils import ex_sequence


def _vocab_missing_string(node:TreeParserNode, display_text: str) -> str:
    return "---" if node.is_dictionary_word(display_text) else ""

def _vocab_node_html(node: TreeParserNode, excluded:set[str], extra: set[str], question:str, answer:str, depth:int) -> str:
    if question in excluded:
        return ""

    priority_class = f"word_priority_{node.get_priority_class(question, extra)}"

    html = f"""
    <li class="sentenceVocabEntry depth{depth} {priority_class}">
        <div class="sentenceVocabEntryDiv">
            <span class="vocabQuestion clipboard">{question}</span>
            <span class="vocabAnswer">{answer}</span>
        </div>
        {_create_html_from_nodes(node.children, excluded, extra, depth + 1)}
    </li>
    """
    return html

def _create_html_from_nodes(nodes: list[TreeParserNode], excluded: set[str], extra: set[str], depth:int) -> str:
    if not nodes:
        return ""

    html = f"""<ul class="sentenceVocabList depth{depth}">\n"""

    for node in nodes:
        vocabs:list[VocabNote] = []
        found_words: set[str] = set()
        if node.is_show_at_all_in_sentence_breakdown():
            vocabs = app.col().vocab.search(search_utils.node_vocab_lookup(node))
            vocabs = [voc for voc in vocabs if voc.get_display_question() not in excluded]
            found_words = set((voc.get_question() for voc in vocabs)) | set(ex_sequence.flatten([voc.get_readings() for voc in vocabs]))

        if vocabs:
            for vocab in vocabs:
                html += _vocab_node_html(node, excluded, extra, vocab.get_display_question(), vocab.get_active_answer(), depth)

            if (node.is_inflected()
                    and node.surface not in found_words
                    and node.surface not in excluded
                    and node.is_show_surface_in_sentence_breakdown()):

                html += _vocab_node_html(node, excluded, extra, node.surface, _vocab_missing_string(node, node.surface), depth)

        else:
            question_text = node.surface if depth == 1 and node.is_inflected() and node.is_probably_not_dictionary_word() else node.base
            html += _vocab_node_html(node, excluded, extra, question_text, _vocab_missing_string(node, question_text), depth)
            if node.is_show_surface_in_sentence_breakdown() and node.surface not in excluded:
                html += _vocab_node_html(node, excluded, extra, node.surface, _vocab_missing_string(node, node.surface), depth)

    html += "</ul>\n"

    return html



def _build_user_extra_list(extra_words: list[str], excluded:set[str]) -> str:
    html = f"""<ul class="sentenceVocabList userExtra depth1">\n"""
    for word in extra_words:
        vocabs = app.col().vocab.search(search_utils.single_vocab_by_form_exact(word))
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


def build_breakdown_html(sentence: SentenceNote) -> str:
    user_excluded = sentence.get_user_excluded_vocab()
    extra_words = sentence.get_user_extra_vocab()
    html = ""
    if extra_words:
        html += _build_user_extra_list(extra_words, user_excluded)

    question = sentence.get_active_question()
    nodes = tree_parser.parse_tree(question, user_excluded).nodes

    user_extra = set(extra_words)
    html += _create_html_from_nodes(nodes, user_excluded, user_extra, 1)

    html += """
    ##KANJI_LIST##
        """

    return html

recent_reviewer_cards = RecentItems[int](1)

def render_breakdown(html:str, card: Card, _type_of_display:str) -> str:
    note = JPNote.note_from_note(card.note())
    if isinstance(note, SentenceNote):
        breakdown_html = build_breakdown_html(note)
        html = html.replace("##VOCAB_BREAKDOWN##", breakdown_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_breakdown)