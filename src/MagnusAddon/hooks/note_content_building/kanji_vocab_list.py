from aqt import gui_hooks

from hooks.note_content_building.content_renderer import PrerenderingAnswerContentRenderer
from note.kanjinote import KanjiNote
from note.vocabnote import VocabNote
from sysutils.ex_str import newline


def generate_vocab_html_list(_kanji_note: KanjiNote) -> str:
    def _create_classes(_kanji: KanjiNote, _vocab: VocabNote) -> str:
        tags = list(_vocab.priority_spec().tags)
        tags.sort()
        classes = " ".join([f"""common_ness_{prio}""" for prio in tags])
        classes += f""" {_vocab.priority_spec().priority_string}"""
        classes += " " + " ".join(_vocab.get_meta_tags())

        if _vocab.get_question() in primary_vocab or (_vocab.get_readings() and _vocab.get_readings()[0] in _kanji.get_primary_vocab()):
            classes += " primary_vocab" if has_real_primary_vocabs else " default_primary_vocab"

        return classes

    vocabs = _kanji_note.get_vocab_notes_sorted()
    primary_vocab = _kanji_note.get_primary_vocabs_or_defaults()
    has_real_primary_vocabs = any(_kanji_note.get_primary_vocab())

    if vocabs:
        return f'''
                <div class="kanjiVocabList page_section">
                    <div class="page_section_title">vocabulary</div>
                    <div>
    
                    {newline.join([f"""
                    <div class="kanjiVocabEntry {_create_classes(_kanji_note, _vocab_note)}">
                        <audio src="{_vocab_note.get_primary_audio_path()}"></audio><a class="play-button"></a>
                        <span class="kanji clipboard">{_vocab_note.get_question()}</span>
                        (<span class="clipboard vocabReading">{", ".join(_kanji_note.tag_vocab_readings(_vocab_note))}</span>)
                        {_vocab_note.get_meta_tags_html()}
                        <span class="meaning"> {_vocab_note.get_answer()}</span>
                    </div>
                    """ for _vocab_note in vocabs])}
    
                    </div>
                </div>
                '''
    else:
        return ''

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(KanjiNote, {"##VOCAB_LIST##": generate_vocab_html_list}).render)
