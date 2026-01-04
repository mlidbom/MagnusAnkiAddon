from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.vocabulary.pos import POS
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabMetaTag(Slots):
    def __init__(self, name: str, display: str, tooltip: str) -> None:
        self.name: str = name
        self.display: str = display
        self.tooltip: str = tooltip

def get_meta_tags_html(vocab: VocabNote, display_extended_sentence_statistics: bool = True, no_sentense_statistics: bool = False) -> str:
    tags = vocab.tags.select(lambda it: it.name).to_set()
    meta: list[VocabMetaTag] = []
    tos = QSet(t.lower().strip() for t in vocab.parts_of_speech.raw_string_value().split(","))

    if not no_sentense_statistics:
        def max_nine_number(value: int) -> str: return f"""{value}""" if value < 10 else "+"
        highlighted_in = vocab.sentences.user_highlighted()
        meta.append(VocabMetaTag("highlighted_in_sentences", f"""{max_nine_number(len(highlighted_in))}""", f"""highlighted in {len(highlighted_in)} sentences"""))

        counts = vocab.sentences.counts()
        if counts.total > 0:
            tooltip_text = f"""in {counts.total} sentences. Studying-listening:{counts.studying_listening}, Studying-reading:{counts.studying_reading}"""
            if counts.studying_listening > 0 or counts.studying_reading > 0:
                if display_extended_sentence_statistics:
                    meta.append(VocabMetaTag("in_studying_sentences", f"""{counts.studying_listening}:{counts.studying_reading}/{counts.total}""", tooltip_text))
                else:
                    def create_display_text() -> str:
                        if counts.studying_listening > 9 and counts.studying_reading > 9:
                            return "+"
                        return f"{max_nine_number(counts.studying_listening)}:{max_nine_number(counts.studying_reading)}/{max_nine_number(counts.total)}"

                    meta.append(VocabMetaTag("in_studying_sentences", create_display_text(), tooltip_text))
            else:
                meta.append(VocabMetaTag("in_sentences", f"""{counts.total}""", tooltip_text))
        else:
            meta.append(VocabMetaTag("in_no_sentences", f"""{counts.total}""", f"""in {counts.total} sentences"""))

    # overarching info
    if "_uk" in tags: meta.append(VocabMetaTag("uk", "uk", "usually written using kana only"))
    if POS.EXPRESSION in tos: meta.append(VocabMetaTag(POS.EXPRESSION, "x", "expression"))
    if POS.ABBREVIATION in tos: meta.append(VocabMetaTag("abbreviation", "abbr", "abbreviation"))
    if POS.AUXILIARY in tos: meta.append(VocabMetaTag("auxiliary", "aux", "auxiliary"))
    if POS.PREFIX in tos: meta.append(VocabMetaTag("prefix", "頭", "prefix"))
    if POS.SUFFIX in tos: meta.append(VocabMetaTag("suffix", "尾", "suffix"))

    # nouns
    if POS.PROPER_NOUN in tos: meta.append(VocabMetaTag("proper-noun", "p-名", "proper noun"))
    if POS.PRONOUN in tos: meta.append(VocabMetaTag("pronoun", "pr-名", "pronoun"))
    if POS.NOUN in tos: meta.append(VocabMetaTag(POS.NOUN, "名", "noun"))
    if POS.ADVERBIAL_NOUN in tos: meta.append(VocabMetaTag("adverbial-noun", "副-名", "adverbial noun"))
    if POS.INDEPENDENT_NOUN in tos: meta.append(VocabMetaTag("independent-noun", "i-名", "independent noun"))

    # verbs
    if POS.ICHIDAN_VERB in tos: meta.append(_create_verb_meta_tag("ichidan", "1", POS.ICHIDAN_VERB, tos))
    if POS.GODAN_VERB in tos: meta.append(_create_verb_meta_tag("godan", "5", POS.GODAN_VERB, tos))
    if POS.SURU_VERB in tos or "verbal noun" in tos or "する verb" in tos: meta.append(_create_verb_meta_tag("suru-verb", "為", POS.SURU_VERB, tos))
    if POS.KURU_VERB in tos: meta.append(_create_verb_meta_tag("kuru-verb", "k-v", "kuru verb", tos))
    if "auxiliary verb" in tos: meta.append(_create_verb_meta_tag("auxiliary-verb", "aux-v", "auxiliary verb", tos))

    # adverbs
    if POS.TO_ADVERB in tos: meta.append(VocabMetaTag("to-adverb", "と", "adverbial noun taking the と particle to act as adverb"))
    elif POS.ADVERB in tos: meta.append(VocabMetaTag("adverb", "副", "adverb"))
    elif POS.ADVERBIAL in tos: meta.append(VocabMetaTag("adverbial", "副", "adverbial"))

    # adjectives
    if POS.I_ADJECTIVE in tos: meta.append(VocabMetaTag("i-adjective", "い", "true adjective ending on the い copula"))
    if POS.NA_ADJECTIVE in tos: meta.append(VocabMetaTag("na-adjective", "な", "adjectival noun taking the な particle to act as adjective"))
    if POS.NO_ADJECTIVE in tos: meta.append(VocabMetaTag("no-adjective", "の", "adjectival noun taking the の particle to act as adjective"))
    if "auxiliary adjective" in tos: meta.append(VocabMetaTag("auxiliary-adjective", "a-い", "auxiliary adjective"))

    # misc

    if POS.COUNTER in tos: meta.append(VocabMetaTag("counter", "ctr", "counter"))
    if POS.NUMERAL in tos: meta.append(VocabMetaTag("numeral", "num", "numeral"))
    if POS.INTERJECTION in tos: meta.append(VocabMetaTag("interjection", "int", "interjection"))
    if POS.CONJUNCTION in tos: meta.append(VocabMetaTag("conjunction", "conj", "conjunction"))
    if POS.PARTICLE in tos: meta.append(VocabMetaTag("particle", "prt", "particle"))

    # my own inventions
    if POS.MASU_SUFFIX in tos: meta.append(VocabMetaTag("masu-suffix", "連", "follows the 連用形/masu-stem form of a verb"))

    return """<ol class="vocab_tag_list">""" + "".join([f"""<li class="vocab_tag vocab_tag_{tag.name}" title="{tag.tooltip}">{tag.display}</li>""" for tag in meta]) + "</ol>"

def _create_verb_meta_tag(name: str, display: str, tooltip: str, tos: QSet[str]) -> VocabMetaTag:
    tag = VocabMetaTag(name, display, tooltip)

    if POS.INTRANSITIVE in tos:
        tag.display += "i"
        tag.tooltip = "intransitive " + tag.tooltip
    if POS.TRANSITIVE in tos:
        tag.display += "t"
        tag.tooltip = "transitive " + tag.tooltip

    return tag
