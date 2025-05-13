from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import NoteFields

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote

class VocabMetaTag:
    def __init__(self, name: str, display: str, tooltip: str) -> None:
        self.name = name
        self.display = display
        self.tooltip = tooltip

def get_meta_tags_html(vocab: VocabNote, display_extended_sentence_statistics: bool = True) -> str:
    tags = set(vocab.get_tags())
    meta: list[VocabMetaTag] = []
    tos = set([t.lower().strip() for t in vocab.parts_of_speech.raw_string_value().split(",")])

    def max_nine_number(value: int) -> str: return f"""{value}""" if value < 10 else "+"
    highlighted_in = vocab.sentences.user_highlighted()
    meta.append(VocabMetaTag("highlighted_in_sentences", f"""{max_nine_number(len(highlighted_in))}""", f"""highlighted in {len(highlighted_in)} sentences"""))

    sentences = vocab.sentences.with_owned_form()
    if sentences:
        studying_sentences_reading = _get_studying_sentence_count(sentences, NoteFields.VocabNoteType.Card.Reading)
        studying_sentences_listening = _get_studying_sentence_count(sentences, NoteFields.VocabNoteType.Card.Listening)
        tooltip_text = f"""in {len(sentences)} sentences. Studying-listening:{studying_sentences_listening}, Studying-reading:{studying_sentences_reading}"""
        if studying_sentences_reading or studying_sentences_listening:
            if display_extended_sentence_statistics:
                meta.append(VocabMetaTag("in_studying_sentences", f"""{studying_sentences_listening}:{studying_sentences_reading}/{len(sentences)}""", tooltip_text))
            else:
                def create_display_text() -> str:
                    if studying_sentences_listening > 9 and studying_sentences_reading > 9:
                        return "+"
                    return f"{max_nine_number(studying_sentences_listening)}:{max_nine_number(studying_sentences_reading)}/{max_nine_number(len(sentences))}"

                meta.append(VocabMetaTag("in_studying_sentences", create_display_text(), tooltip_text))
        else:
            meta.append(VocabMetaTag("in_sentences", f"""{len(sentences)}""", tooltip_text))
    else:
        meta.append(VocabMetaTag("in_no_sentences", f"""{len(sentences)}""", f"""in {len(sentences)} sentences"""))

    # overarching info
    if "_uk" in tags: meta.append(VocabMetaTag("uk", "uk", "usually written using kana only"))
    if "expression" in tos: meta.append(VocabMetaTag("expression", "x", "expression"))
    if "abbreviation" in tos: meta.append(VocabMetaTag("abbreviation", "abbr", "abbreviation"))
    if "auxiliary" in tos: meta.append(VocabMetaTag("auxiliary", "aux", "auxiliary"))
    if "prefix" in tos: meta.append(VocabMetaTag("prefix", "頭", "prefix"))
    if "suffix" in tos: meta.append(VocabMetaTag("suffix", "尾", "suffix"))

    # nouns
    if "proper noun" in tos: meta.append(VocabMetaTag("proper-noun", "p-名", "proper noun"))
    elif "pronoun" in tos: meta.append(VocabMetaTag("pronoun", "pr-名", "pronoun"))
    elif "noun" in tos: meta.append(VocabMetaTag("noun", "名", "noun"))
    if "adverbial noun" in tos: meta.append(VocabMetaTag("adverbial-noun", "副-名", "adverbial noun"))
    if "independent noun" in tos: meta.append(VocabMetaTag("independent-noun", "i-名", "independent noun"))

    # verbs
    if "ichidan verb" in tos: meta.append(_create_verb_meta_tag("ichidan", "1", "ichidan verb", tos))
    if "godan verb" in tos: meta.append(_create_verb_meta_tag("godan", "5", "godan verb", tos))
    if "suru verb" in tos or "verbal noun" in tos or "する verb" in tos: meta.append(_create_verb_meta_tag("suru-verb", "為", "suru verb", tos))
    if "kuru verb" in tos: meta.append(_create_verb_meta_tag("kuru-verb", "k-v", "kuru verb", tos))
    if "auxiliary verb" in tos: meta.append(_create_verb_meta_tag("auxiliary-verb", "aux-v", "auxiliary verb", tos))

    # adverbs
    if "と adverb" in tos or "to-adverb" in tos: meta.append(VocabMetaTag("to-adverb", "と", "adverbial noun taking the と particle to act as adverb"))
    elif "adverb" in tos: meta.append(VocabMetaTag("adverb", "副", "adverb"))
    elif "adverbial" in tos: meta.append(VocabMetaTag("adverbial", "副", "adverbial"))

    # adjectives
    if "い adjective" in tos or "i-adjective" in tos: meta.append(VocabMetaTag("i-adjective", "い", "true adjective ending on the い copula"))
    if "な adjective" in tos or "na-adjective" in tos: meta.append(VocabMetaTag("na-adjective", "な", "adjectival noun taking the な particle to act as adjective"))
    if "の adjective" in tos or "no-adjective" in tos: meta.append(VocabMetaTag("no-adjective", "の", "adjectival noun taking the の particle to act as adjective"))
    if "auxiliary adjective" in tos: meta.append(VocabMetaTag("auxiliary-adjective", "aux-adj", "auxiliary adjective"))

    # ???
    if "in compounds" in tos: meta.append(VocabMetaTag("in-compounds", "i-c", "in compounds"))

    # misc

    if "counter" in tos: meta.append(VocabMetaTag("counter", "ctr", "counter"))
    if "numeral" in tos: meta.append(VocabMetaTag("numeral", "num", "numeral"))
    if "interjection" in tos: meta.append(VocabMetaTag("interjection", "int", "interjection"))
    if "conjunction" in tos: meta.append(VocabMetaTag("conjunction", "conj", "conjunction"))
    if "particle" in tos: meta.append(VocabMetaTag("particle", "prt", "particle"))

    # my own inventions
    if "masu-suffix" in tos: meta.append(VocabMetaTag("masu-suffix", "連", "follows the 連用形/masu-stem form of a verb"))

    return """<ol class="vocab_tag_list">""" + "".join([f"""<li class="vocab_tag vocab_tag_{tag.name}" title="{tag.tooltip}">{tag.display}</li>""" for tag in meta]) + "</ol>"

def _create_verb_meta_tag(name: str, display: str, tooltip: str, tos: set[str]) -> VocabMetaTag:
    tag = VocabMetaTag(name, display, tooltip)

    if "intransitive verb" in tos or "intransitive" in tos:
        tag.display += "i"
        tag.tooltip = "intransitive " + tag.tooltip
    if "transitive verb" in tos or "transitive" in tos:
        tag.display += "t"
        tag.tooltip = "transitive " + tag.tooltip

    return tag

def _get_studying_sentence_count(sentences: list[SentenceNote], card: str = "") -> int:
    return len([sentence for sentence in sentences if sentence.is_studying(card)])