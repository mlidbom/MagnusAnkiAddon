from aqt import gui_hooks

from ankiutils import app
from hooks.note_content_building.content_renderer import PrerenderingAnswerContentRenderer
from language_services.janome_ex.word_extraction import word_extractor
from language_services.shared import priorities
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import kana_utils

def _build_vocab_list(word_to_show: list[str], excluded_words:set[str], title:str, include_extended_sentence_statistics:bool = False) -> str:
    html = f"""
    <div class="breakdown page_section">
        <div class="page_section_title">{title}</div>
        <ul class="sentenceVocabList userExtra depth1">
"""
    for word in (w for w in word_to_show if not w in excluded_words):
        vocabs: list[VocabNote] = app.col().vocab.with_form(word)

        vocabs = [voc for voc in vocabs if not voc.get_question() in excluded_words]

        exact_match = [voc for voc in vocabs if voc.get_question() == word]
        if exact_match:
            vocabs = exact_match

        if vocabs:
            for vocab in vocabs:
                hit_form = vocab.get_question() if vocab.get_question() != word else ""
                needs_reading = kana_utils.contains_kanji(word) and (not hit_form or kana_utils.contains_kanji(hit_form))
                readings = ", ".join(vocab.get_readings()) if needs_reading else ""
                html += f"""
                        <li class="sentenceVocabEntry depth1 word_priority_{priorities.very_high} {" ".join(vocab.get_meta_tags())}">
                            <div class="sentenceVocabEntryDiv">
                                <audio src="{vocab.get_primary_audio_path()}"></audio><a class="play-button"></a>
                                <span class="vocabQuestion clipboard">{word}</span>
                                {f'''<span class="vocabHitForm clipboard">{hit_form}</span>''' if hit_form else ""}
                                {f'''<span class="vocabHitReadings clipboard">{readings}</span>''' if readings else ""}
                                {vocab.get_meta_tags_html(include_extended_sentence_statistics)}
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

def render_parsed_words(note: SentenceNote, replacements:dict[str, str]) ->None:
    hierarchy = word_extractor.extract_words_hierarchical(note.get_question(), note.get_user_excluded_vocab())
    only_roots = [w.word.word for w in hierarchy]

    replacements["##PARSED_WORDS##"] = _build_vocab_list(only_roots, note.get_user_excluded_vocab(), "parsed words")

def render_excluded_words(note: SentenceNote, replacements:dict[str, str]) ->None:
    replacements["##EXCLUDED_WORDS##"] = _build_vocab_list(list(note.get_user_excluded_vocab()), set(), "incorrectly matched words")

def render_user_extra_list(note: SentenceNote, replacements:dict[str, str]) ->None:
    replacements["##USER_EXTRA_VOCAB##"] = _build_vocab_list(note.get_user_highlighted_vocab(), note.get_user_excluded_vocab(), "highlighted words", include_extended_sentence_statistics=True) if note.get_user_highlighted_vocab() else ""


def render(note: SentenceNote) -> dict[str, str]:
    replacements:dict[str, str] = {}

    render_parsed_words(note, replacements)
    render_user_extra_list(note, replacements)
    render_excluded_words(note, replacements)


    return replacements

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, render).render)
