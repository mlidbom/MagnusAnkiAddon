from aqt import gui_hooks

from ankiutils import app
from hooks.note_content_building.content_renderer import PrerenderingAnswerContentRenderer
from language_services.jamdict_ex.dict_lookup import DictLookup
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import kana_utils
from sysutils.ex_str import newline

def _build_vocab_list(word_to_show: list[str], excluded_words:set[str], title:str, include_mnemonics:bool = False, show_words_missing_dictionary_entries:bool=False, include_extended_sentence_statistics:bool = False) -> str:
    html = f"""
    <div class="breakdown page_section">
        <div class="page_section_title">{title}</div>
        <ul class="sentenceVocabList userExtra depth1">
"""
    for word in (w for w in word_to_show if w not in excluded_words):
        vocabs = lookup_vocabs(excluded_words, word)

        if vocabs:
            for vocab in vocabs:
                hit_form = vocab.get_question() if vocab.get_question() != word else ""
                needs_reading = kana_utils.contains_kanji(word) and (not hit_form or kana_utils.contains_kanji(hit_form))
                readings = ", ".join(vocab.get_readings()) if needs_reading else ""
                html += f"""
                        <li class="sentenceVocabEntry depth1 word_priority_very_high {" ".join(vocab.get_meta_tags())}">
                            <div class="sentenceVocabEntryDiv">
                                <audio src="{vocab.get_primary_audio_path()}"></audio><a class="play-button"></a>
                                <span class="vocabQuestion clipboard">{word}</span>
                                {f'''<span class="vocabHitForm clipboard">{hit_form}</span>''' if hit_form else ""}
                                {f'''<span class="vocabHitReadings clipboard">{readings}</span>''' if readings else ""}
                                {vocab.get_meta_tags_html(include_extended_sentence_statistics)}
                                <span class="vocabAnswer">{vocab.get_answer()}</span>
                            </div>
                            {f'''<div class="sentenceVocabEntryMnemonic">{ vocab.get_mnemonics_override() }</div>''' if include_mnemonics and vocab.get_mnemonics_override() and vocab.get_mnemonics_override() != '-' else '' }
                        </li>
                        """
        else:
            class Hit:
                def __init__(self, forms:str, readings:str, answer:str):
                    self.forms: str = forms
                    self.readings: str = readings
                    self.answer = answer

            dictionary_hits = [Hit(forms=",".join(hit.valid_forms()), readings=",".join(f.text for f in hit.entry.kana_forms), answer=hit.generate_answer()) for hit in DictLookup.lookup_word_shallow(word).entries]

            if not dictionary_hits and show_words_missing_dictionary_entries:
                dictionary_hits = [Hit(word, "", "---")]

            html += newline.join(f"""
                        <li class="sentenceVocabEntry depth1 word_priority_very_low">
                            <div class="sentenceVocabEntryDiv">
                                <span class="vocabQuestion clipboard">{word}</span>
                                {f'''<span class="vocabHitForm clipboard">{hit.forms}</span>''' if hit.forms != word else ""} 
                                <span class="vocabHitReadings clipboard">{hit.readings}</span>
                                <span class="vocabAnswer">{hit.answer}</span>
                            </div>
                        </li>
""" for hit in dictionary_hits)

    html += """</ul>
        </div>
    """
    return html

def lookup_vocabs(excluded_words: set[str], word:str) -> list[VocabNote]:
    vocabs: list[VocabNote] = app.col().vocab.with_form(word)
    vocabs = [voc for voc in vocabs if not voc.get_question() in excluded_words]
    exact_match = [voc for voc in vocabs if voc.get_question_without_noise_characters() == word]
    if exact_match:
        vocabs = exact_match
    return vocabs

def render_parsed_words(note: SentenceNote) -> str:
    words = note.get_valid_parsed_non_child_words_strings()
    excluded = note.get_user_excluded_vocab()
    return _build_vocab_list(words, excluded, "parsed words")

def render_words_missing_dictionary_entries(note: SentenceNote) -> str:
    words = note.get_valid_parsed_non_child_words_strings()
    excluded_words = note.get_user_excluded_vocab()

    def has_vocab(word:str) -> bool:
        vocabs = lookup_vocabs(excluded_words, word)
        return len(vocabs) > 0 or len(DictLookup.lookup_word_shallow(word).entries) > 0


    words_without_dictionary_entries = [word for word in words if not has_vocab(word)]

    return _build_vocab_list(words_without_dictionary_entries, set(), "matched words without dictionary entries", show_words_missing_dictionary_entries=True) if words_without_dictionary_entries else ""

def render_excluded_words(note: SentenceNote) -> str:
    excluded_words = {x.word for x in note.get_user_word_exclusions()}
    excluded_vocab = list(excluded_words)
    return _build_vocab_list(excluded_vocab, set(), "incorrectly matched words", show_words_missing_dictionary_entries=True) if excluded_vocab else ""

def render_user_extra_list(note: SentenceNote) -> str:
    return _build_vocab_list(note.get_user_highlighted_vocab(), note.get_user_excluded_vocab(), "highlighted words", include_mnemonics=True, show_words_missing_dictionary_entries=True, include_extended_sentence_statistics=True) if note.get_user_highlighted_vocab() else ""

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {
        "##PARSED_WORDS##": render_parsed_words,
        "##EXCLUDED_WORDS##": render_excluded_words,
        "##USER_EXTRA_VOCAB##": render_user_extra_list,
        "##WORDS_MISSING_DICTIONARY_ENTRIES##": render_words_missing_dictionary_entries,
    }).render)
