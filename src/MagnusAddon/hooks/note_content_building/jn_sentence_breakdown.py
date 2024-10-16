# todo remove this file
from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app, ui_utils
from ankiutils.app import ui_utils
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from language_services.janome_ex.tree_building import jn_tree_builder
from language_services.janome_ex.tree_building.tree_parser_node import TreeParserNode
from language_services.shared import priorities
from sysutils import ex_sequence
from sysutils.collections.recent_items import RecentItems

def _vocab_missing_string(node: TreeParserNode, display_text: str) -> str:
    return "---" if node.is_dictionary_word(display_text) else ""

def _vocab_node_html(node: TreeParserNode, excluded: set[str], extra: set[str], question: str, answer: str, depth: int) -> str:
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

def _create_html_from_nodes(nodes: list[TreeParserNode], excluded: set[str], extra: set[str], depth: int) -> str:
    if not nodes:
        return ""

    html = f"""<ul class="sentenceVocabList depth{depth}">\n"""

    for node in nodes:
        vocabs: list[VocabNote] = []
        found_words: set[str] = set()
        if node.is_show_at_all_in_sentence_breakdown():
            if node.is_show_base_in_sentence_breakdown():
                vocabs += app.col().vocab.with_form(node.base)

            if node.is_show_surface_in_sentence_breakdown():
                vocabs += app.col().vocab.with_form(node.surface)

            vocabs = [voc for voc in vocabs if voc.get_display_question() not in excluded]
            found_words = set((voc.get_question() for voc in vocabs)) | set(ex_sequence.flatten([voc.get_readings() for voc in vocabs]))

        if vocabs:
            for voc in vocabs:
                html += _vocab_node_html(node, excluded, extra, voc.get_display_question(), voc.get_answer(), depth)

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

def _build_user_extra_list(extra_words: list[str], excluded: set[str]) -> str:
    html = f"""<ul class="sentenceVocabList userExtra depth1">\n"""
    for word in extra_words:
        vocabs: list[VocabNote] = app.col().vocab.with_form(word)
        vocabs = [voc for voc in vocabs if voc.get_display_question() not in excluded]

        if vocabs:
            for vocab in vocabs:
                html += f"""
                    <li class="sentenceVocabEntry depth1 word_priority_{priorities.very_high}">
                        <div class="sentenceVocabEntryDiv">
                            <span class="vocabQuestion clipboard">{vocab.get_display_question()}</span>
                            {vocab.get_meta_tags_html()}
                            <span class="vocabAnswer">{vocab.get_answer()}</span>
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

recent_reviewer_cards = RecentItems[int](1)

def render_breakdown(html: str, card: Card, _type_of_display: str) -> str:
    if not ui_utils.is_displaytype_displaying_answer(_type_of_display):
        return html

    note = JPNote.note_from_note(card.note())
    if isinstance(note, SentenceNote):
        user_excluded = note.get_user_excluded_vocab()
        extra_words = note.get_user_highlighted_vocab()
        if extra_words:
            user_extra_html = _build_user_extra_list(extra_words, user_excluded)
            html = html.replace("##USER_EXTRA_VOCAB##", user_extra_html)

        question = note.get_question()
        nodes = jn_tree_builder.parse_tree(question, user_excluded).nodes
        user_extra = set(extra_words)
        breakdown_html = _create_html_from_nodes(nodes, user_excluded, user_extra, 1)
        html = html.replace("##VOCAB_BREAKDOWN##", breakdown_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_breakdown)
