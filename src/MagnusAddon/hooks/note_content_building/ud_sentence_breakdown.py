from aqt import gui_hooks

from ankiutils import app
from hooks.note_content_building.content_renderer import PrerenderingAnswerContentRenderer
from language_services.shared import priorities
from language_services.universal_dependencies import ud_tokenizers
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import kana_utils
from viewmodels.sentence_breakdown import sentence_breakdown_viewmodel
from viewmodels.sentence_breakdown.sentence_breakdown_viewmodel import NodeViewModel, VocabHit

def _node_html(node: NodeViewModel, excluded: set[str], highlighted: set[str], depth: int) -> str:
    def priority_class(question: str) -> str:
        return "word_priority_" + node.get_priority_class(question, highlighted)

    html = ""

    vocab_hits:list[VocabHit] = node.surface_vocab_hits + node.base_vocab_hits
    vocab_hits = [voc for voc in vocab_hits if voc.hit_form not in excluded]
    exact_match = [voc for voc in vocab_hits if voc.is_exact_match()]
    if exact_match:
        vocab_hits = [exact_match[0]]

    if vocab_hits:
        for vocab_entry in vocab_hits:
            needs_reading = True #I need to practice katakana #kana_utils.contains_kanji(vocab_entry.lookup_form) and (not vocab_entry.hit_form or kana_utils.contains_kanji(vocab_entry.hit_form))
            readings = ", ".join(vocab_entry.readings) if needs_reading else ""
            readings = kana_utils.to_katakana(readings)
            html += f"""
            <li class="sentenceVocabEntry depth{depth} {vocab_entry.meta_tags} {priority_class(vocab_entry.lookup_form if vocab_entry.lookup_form else vocab_entry.surface_form)}">
                <div class="sentenceVocabEntryDiv">
                    <span class="vocabQuestion clipboard">{vocab_entry.surface_form}</span>
                    {f'''<span class="vocabLookupForm {'' if vocab_entry.hit_form else 'vocabHitForm' } clipboard">{vocab_entry.lookup_form}</span>''' if vocab_entry.lookup_form else ""}
                    {f'''<span class="vocabHitForm clipboard">{vocab_entry.hit_form}</span>''' if vocab_entry.hit_form else ""}
                    {f'''<span class="vocabHitReadings clipboard">{readings}</span>''' if readings else ""}
                    {vocab_entry.meta_tags_html}
                    
                    
                    <span class="vocabAnswer">{vocab_entry.answer}</span>
                </div>
                {_create_html_from_nodes(node.children, excluded, highlighted, depth + 1)}
            </li>
            """
    else:
        html += f"""
            <li class="sentenceVocabEntry depth{depth} {priority_class(node.surface)}">
                <div class="sentenceVocabEntryDiv">
                    <span class="vocabQuestion clipboard">{node.surface}</span>
                </div>
                {_create_html_from_nodes(node.children, excluded, highlighted, depth + 1)}
            </li>
            """

    return html

def _build_user_extra_list(extra_words: list[str], user_excluded:set[str]) -> str:
    html = f"""
    <div class="breakdown page_section">
        <div class="page_section_title">extra vocab</div>
        <ul class="sentenceVocabList userExtra depth1">
"""
    for word in extra_words:
        vocabs: list[VocabNote] = app.col().vocab.with_form(word)

        vocabs = [voc for voc in vocabs if not voc.get_question() in user_excluded]

        exact_match = [voc for voc in vocabs if voc.get_question() == word]
        if exact_match:
            vocabs = exact_match

        if vocabs:
            for vocab in vocabs:
                hit_form = vocab.get_question() if vocab.get_question() != word else ""
                needs_reading = True #I need to practice katakana # kana_utils.contains_kanji(word) and (not hit_form or kana_utils.contains_kanji(hit_form))
                readings = ", ".join(vocab.get_readings()) if needs_reading else ""
                readings = kana_utils.to_katakana(readings)
                html += f"""
                        <li class="sentenceVocabEntry depth1 word_priority_{priorities.very_high} {" ".join(vocab.get_meta_tags())}">
                            <div class="sentenceVocabEntryDiv">
                                <audio src="{vocab.get_primary_audio_path()}"></audio><a class="play-button"></a>
                                <span class="vocabQuestion clipboard">{word}</span>
                                {f'''<span class="vocabHitForm clipboard">{hit_form}</span>''' if hit_form else ""}
                                {f'''<span class="vocabHitReadings clipboard">{readings}</span>''' if readings else ""}
                                {vocab.get_meta_tags_html()}
                                <span class="vocabAnswer">{vocab.get_answer()}</span>
                            </div>
                            {f'''<div class="sentenceVocabEntryMnemonic">{ vocab.get_mnemonics_override() }</div>''' if vocab.get_mnemonics_override() and vocab.get_mnemonics_override() != '-' else '' }
                        </li>
                        """
        else:
            html += f"""
                        <li class="sentenceVocabEntry depth1 word_priority_{priorities.very_high}">
                           <div class="sentenceVocabEntryDiv">
                               <span class="vocabQuestion clipboard">{word}</span>
                               <span class="vocabAnswer">---</span>
                           </div>
                        </li>
                        """

    html += """</ul>
        </div>
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

def print_debug_information_for_analysis(sentence: str) -> str:
    html = f"""<div id="debug_output">\n"""

    for parser in ud_tokenizers.all_tokenizers:
        html += f"""{parser.name} : {sentence}
{parser.tokenize(sentence).str_()}

"""

    for parser in ud_tokenizers.all_tokenizers:
        html += f"""{parser.name} : {sentence}
{parser.tokenize(sentence).to_tree()}

"""

    for parser in ud_tokenizers.all_tokenizers:
        html += f"""{parser.name} : {sentence}")
{ud_tree_builder.build_tree(parser, sentence)}

"""

    html += """</div>\n"""

    return html

def render_parsed_words(note: SentenceNote) -> dict[str, str]:
    detected_words = note.get_parsed_words()



    return {}

# noinspection DuplicatedCode
def render_breakdown(note: SentenceNote) -> dict[str, str]:
    replacements:dict[str, str] = {}

    user_excluded = note.get_user_excluded_vocab()
    extra_words = note.get_user_highlighted_vocab()
    question = note.get_question()
    tree = ud_tree_builder.build_tree(ud_tokenizers.default, question)
    view_model = sentence_breakdown_viewmodel.create(tree, app.col())

    replacements["##USER_EXTRA_VOCAB##"] = _build_user_extra_list(extra_words, user_excluded) if extra_words else ""

    user_higlighted = set(extra_words)
    breakdown_html = f"""
<div class="breakdown page_section">
<div class="page_section_title">breakdown</div>
{_create_html_from_nodes(view_model.nodes, user_excluded, user_higlighted, 1)}
</div>
"""
    #todo: restore this or remove the related code
    # html += f"""
    #
    # {print_debug_information_for_analysis(sentence.get_question())}
    # """
    replacements["##VOCAB_BREAKDOWN##"] = breakdown_html

    return replacements

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, render_breakdown).render)
