from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app
from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from note.jpnote import JPNote
from note.sentencenote import SentenceNote
from viewmodels.sentence_breakdown import sentence_breakdown_viewmodel
from viewmodels.sentence_breakdown.sentence_breakdown_viewmodel import NodeViewModel

def _node_html(node: NodeViewModel, excluded: set[str], extra: set[str], depth: int) -> str:
    priority_class = "word_priority_medium"  # todo fix this

    html = ""

    vocab_hits = node.surface_vocab_hits + node.base_vocab_hits

    if vocab_hits:
        for vocab_entry in vocab_hits:
            html += f"""
            <li class="sentenceVocabEntry depth{depth} {priority_class}">
                <div class="sentenceVocabEntryDiv">
                    <span class="vocabQuestion clipboard">{vocab_entry.surface_form}</span>
                    {f'''<span class="vocabLookupForm clipboard">{vocab_entry.lookup_form}</span>''' if vocab_entry.lookup_form else ""}
                    {f'''<span class="vocabHitForm clipboard">{vocab_entry.hit_form}</span>''' if vocab_entry.hit_form else ""}
                    <span class="vocabAnswer">{vocab_entry.answer}</span>
                </div>
                {_create_html_from_nodes(node.children, excluded, extra, depth + 1)}
            </li>
            """
    else:
        html += f"""
            <li class="sentenceVocabEntry depth{depth} {priority_class}">
                <div class="sentenceVocabEntryDiv">
                    <span class="vocabQuestion clipboard">{node.surface}</span>
                </div>
                {_create_html_from_nodes(node.children, excluded, extra, depth + 1)}
            </li>
            """

    return html

def _create_html_from_nodes(nodes: list[NodeViewModel], excluded: set[str], extra: set[str], depth: int) -> str:
    if not nodes:
        return ""

    html = f"""<ul class="sentenceVocabList depth{depth}">\n"""

    for node in nodes:
        html += _node_html(node, excluded, extra, depth)

    html += "</ul>\n"

    return html

def build_breakdown_html(sentence: SentenceNote) -> str:
    user_excluded = sentence.get_user_excluded_vocab()
    extra_words = sentence.get_user_extra_vocab()
    html = ""

    question = sentence.get_question()
    tree = ud_tree_builder.build_tree(ud_parsers.best, question)
    view_model = sentence_breakdown_viewmodel.create(tree, app.col())

    user_extra = set(extra_words)
    html += _create_html_from_nodes(view_model.nodes, user_excluded, user_extra, 1)

    html += """
    ##KANJI_LIST##
        """

    return html

# noinspection DuplicatedCode
def render_breakdown(html: str, card: Card, _type_of_display: str) -> str:
    note = JPNote.note_from_note(card.note())
    if isinstance(note, SentenceNote) and _type_of_display in {'reviewAnswer', 'previewAnswer'}:
        breakdown_html = build_breakdown_html(note)
        html = html.replace("##VOCAB_BREAKDOWN##", breakdown_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_breakdown)
