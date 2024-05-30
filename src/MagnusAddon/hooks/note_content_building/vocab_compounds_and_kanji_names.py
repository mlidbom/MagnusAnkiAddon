from anki.cards import Card
from aqt import gui_hooks

from ankiutils import app, ui_utils
from language_services.shared import priorities
from note.jpnote import JPNote
from note.kanjinote import KanjiNote
from note.vocabnote import VocabNote
from sysutils import ex_str, kana_utils

# noinspection DuplicatedCode
def _build_compound_list(compounds: list[str]) -> str:
    html = f"""<ul class="vocabCompoundList">\n"""
    for word in compounds:
        vocabs: list[VocabNote] = app.col().vocab.with_form(word)

        if vocabs:
            for vocab in vocabs:
                hit_form = vocab.get_question() if vocab.get_question() != word else ""
                needs_reading = True  # I need to practice katakana # kana_utils.contains_kanji(word) and (not hit_form or kana_utils.contains_kanji(hit_form))
                readings = ", ".join(vocab.get_readings()) if needs_reading else ""
                readings = kana_utils.to_katakana(readings)
                html += f"""
                        <li class="vocabCompound">
                            <div class="vocabCompoundDiv">
                                <span class="vocabCompoundQuestion clipboard">{word}</span>
                                {f'''<span class="vocabCompoundHitForm clipboard">{hit_form}</span>''' if hit_form else ""}
                                {f'''<span class="vocabHitReadings clipboard">{readings}</span>''' if readings else ""}
                                <span class="vocabAnswer">{vocab.get_answer()}</span>
                            </div>
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

    html += "</ul>\n"
    return html


def render_compound_list(html: str, card: Card, _type_of_display: str) -> str:
    vocab_note = JPNote.note_from_note(card.note())
    if isinstance(vocab_note, VocabNote) and ui_utils.is_displaytype_displaying_answer(_type_of_display):
        compounds = vocab_note.get_user_compounds()
        compound_list_html = _build_compound_list(compounds)
        html = html.replace("##VOCAB_COMPOUNDS##", compound_list_html)

        html = render_kanji_names(vocab_note, html)

    return html


def render_kanji_names(vocab_note: VocabNote, html: str) -> str:
    def prepare_kanji_meaning(kanji: KanjiNote) -> str:
        meaning = kanji.get_answer()
        meaning = ex_str.strip_html_and_bracket_markup(meaning)
        meaning = meaning.strip().replace(",", "/").replace(" ", "")
        return meaning

    kanji_list = [char for char in ex_str.extract_characters(vocab_note.get_question()) if kana_utils.is_kanji(char)]

    kanji_names:list[str] = list()
    for kanji_character in kanji_list:
        kanji_note = app.col().kanji.with_kanji(kanji_character)
        if kanji_note:
            kanji_names.append(prepare_kanji_meaning(kanji_note))
        else:
            kanji_names.append("MISSING KANJI")

    html = html.replace("##KANJI_NAMES##", " # ".join(kanji_names))

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_compound_list)
