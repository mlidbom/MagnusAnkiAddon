from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional

import language_services.conjugator
from anki.notes import Note
from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.jamdict_ex.priority_spec import PrioritySpec
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.kanavocabnote import KanaVocabNote
from note.note_constants import Mine, NoteFields, NoteTypes
from note.notefields.string_field import StringField
from note.vocabnote_cloner import VocabCloner
from sysutils import ex_sequence, ex_str, kana_utils
from wanikani.wanikani_api_client import WanikaniClient

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from note.sentencenote import SentenceNote
    from wanikani_api import models


def sort_vocab_list_by_studying_status(vocabs: list[VocabNote], primary_voc: Optional[list[str]] = None, preferred_kanji: Optional[str] = None) -> list[VocabNote]:
    def prefer_primary_vocab_in_order(local_vocab: VocabNote) -> int:
        for index, primary in enumerate(_primary_voc):
            if local_vocab.get_question() == primary or local_vocab.get_question_without_noise_characters() == primary or (local_vocab.get_readings() and local_vocab.get_readings()[0] == primary):
                return index

        return 1000

    def prefer_vocab_with_kanji(local_vocab: VocabNote) -> int:
        return 0 if preferred_kanji is None or preferred_kanji in local_vocab.get_question() else 1

    def prefer_studying_vocab(local_vocab: VocabNote) -> int:
        return 1 if local_vocab.is_studying() else 2

    def prefer_studying_sentences(local_vocab: VocabNote) -> int:
        return 1 if local_vocab.get_sentences_studying() else 2

    def prefer_more_sentences(local_vocab: VocabNote) -> int:
        return -len(local_vocab.get_sentences())

    def prefer_high_priority(_vocab: VocabNote) -> int:
        return _vocab.priority_spec().priority

    _primary_voc = primary_voc if primary_voc else []

    result = vocabs.copy()

    result.sort(key=lambda local_vocab: (prefer_vocab_with_kanji(local_vocab),
                                         prefer_primary_vocab_in_order(local_vocab),
                                         prefer_studying_vocab(local_vocab),
                                         prefer_studying_sentences(local_vocab),
                                         prefer_more_sentences(local_vocab),
                                         prefer_high_priority(local_vocab),
                                         local_vocab.get_question()))

    return result

class VocabMetaTag:
    def __init__(self, name: str, display: str, tooltip: str):
        self.name = name
        self.display = display
        self.tooltip = tooltip

class VocabNote(KanaVocabNote):
    def __init__(self, note: Note):
        super().__init__(note)
        self.cloner = VocabCloner(self)
        self.user_mnemonic = StringField(self, NoteFields.Vocab.Mnemonic__)

    def __repr__(self) -> str: return f"""{self.get_question()}"""

    def set_kanji(self, value: str) -> None: self.set_field(NoteFields.Vocab.Kanji, value)

    _forms_exclusions = re.compile(r'\[\[.*]]')
    def _is_excluded_form(self, form: str) -> bool:
        return bool(self._forms_exclusions.search(form))

    def get_forms(self) -> set[str]: return set(self.get_forms_list())
    def get_forms_without_noise_characters(self) -> set[str]: return set(self.get_forms_list_without_noise_characters())
    def get_forms_list(self) -> list[str]: return [form for form in ex_str.extract_comma_separated_values(self._get_forms()) if not self._is_excluded_form(form)]
    def get_forms_list_without_noise_characters(self) -> list[str]: return [self._strip_noise_characters(form) for form in self.get_forms_list()]
    def get_excluded_forms(self) -> set[str]: return set(form.replace("[[", "").replace("]]", "") for form in ex_str.extract_comma_separated_values(self._get_forms()) if self._is_excluded_form(form))
    def set_forms(self, forms: set[str]) -> None: self._set_forms(", ".join([form.strip() for form in forms]))
    def _get_forms(self) -> str: return self.get_field(NoteFields.Vocab.Forms)
    def _set_forms(self, value: str) -> None: self.set_field(NoteFields.Vocab.Forms, value)
    def get_user_compounds(self) -> list[str]: return ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.user_compounds))
    def set_user_compounds(self, compounds: list[str]) -> None:
        self.set_field(NoteFields.Vocab.user_compounds, ",".join(compounds))

    def in_compounds(self) -> list[VocabNote]:
        from ankiutils import app
        return app.col().vocab.with_compound_part(self.get_question_without_noise_characters())

    def get_direct_dependencies(self) -> set[JPNote]:
        return (set(self.collection.kanji.with_any_kanji_in(list(self.extract_main_form_kanji()))) |
                set(ex_sequence.flatten([self.collection.vocab.with_question(compound_part) for compound_part in self.get_user_compounds()])))

    def update_generated_data(self) -> None:
        self.set_field(NoteFields.Vocab.sentence_count, str(len(self.get_sentences())))

        from language_services.jamdict_ex.dict_lookup import DictLookup

        super().update_generated_data()

        question = self.get_question_without_noise_characters().strip()
        readings = ",".join(self.get_readings())

        if not readings and kana_utils.is_only_kana(question):
            self.set_readings([question])
            self.set_tag(Mine.Tags.UsuallyKanaOnly)

        if len(self.get_user_compounds()) == 0 and self._is_suru_verb_included():
            self.set_user_compounds([question[:-2], "する"])

        if self.get_question():
            lookup = DictLookup.try_lookup_vocab_word_or_name(self)
            if lookup.is_uk() and not self.has_tag(Mine.Tags.DisableKanaOnly):
                self.set_tag(Mine.Tags.UsuallyKanaOnly)

            if not self.get_forms():
                if lookup.found_words():
                    self.set_forms(lookup.valid_forms(self.is_uk()))

                if self.get_question() not in self.get_forms():
                    self.set_forms(self.get_forms() | {self.get_question()})

                if self.is_uk() and self.get_readings()[0] not in self.get_forms():
                    self.set_forms(self.get_forms() | set(self.get_readings()))

            speech_types = self.get_speech_types() - {'Unknown',
                                                      'Godan verbIchidan verb'  # crap inserted by bug in yomitan
                                                      }
            if len(speech_types) == 0:
                self.auto_set_speech_type()

    def _is_suru_verb_included(self) -> bool:
        question = self.get_question_without_noise_characters()
        return question[-2:] == "する"

    def auto_set_speech_type(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup

        lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if lookup.found_words():
            self.set_speech_type(", ".join(lookup.parts_of_speech()))
        elif self._is_suru_verb_included():
            question = self.get_question_without_noise_characters()[:-2]
            readings = [reading[:-2] for reading in self.get_readings()]
            lookup = DictLookup.try_lookup_word_or_name(question, readings)
            pos = lookup.parts_of_speech() & {"transitive", "intransitive"}
            self.set_speech_type("suru verb, " + ", ".join(pos))

    def extract_main_form_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    def extract_all_kanji(self) -> set[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question() + self._get_forms())
        return set(char for char in clean if kana_utils.character_is_kanji(char))

    def is_uk(self) -> bool: return self.has_tag(Mine.Tags.UsuallyKanaOnly)

    def set_reading_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_reading_mnemonic, value)

    def get_readings(self) -> list[str]: return ex_str.extract_comma_separated_values(self._get_reading())
    def set_readings(self, readings: list[str]) -> None: self._set_reading(", ".join([reading.strip() for reading in readings]))

    def _get_reading(self) -> str: return self.get_field(NoteFields.Vocab.Reading)
    def _set_reading(self, value: str) -> None: self.set_field(NoteFields.Vocab.Reading, value)

    def set_component_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Vocab.component_subject_ids, value)

    def priority_spec(self) -> PrioritySpec:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        return lookup.priority_spec() if lookup else PrioritySpec(set())

    def get_primary_audio(self) -> str:
        if self.get_audio_male():
            return self.get_audio_male()
        elif self.get_audio_female():
            return self.get_audio_female()
        else:
            return ""

    def get_primary_audio_path(self) -> str:
        primary_audio = self.get_primary_audio().strip()
        if not primary_audio:
            return ""

        primary_list = primary_audio.replace("[sound:", "").split("]")
        return primary_list[0]

    @staticmethod
    def _create_verb_meta_tag(name: str, display: str, tooltip: str, tos: set[str]) -> VocabMetaTag:
        tag = VocabMetaTag(name, display, tooltip)

        if "intransitive verb" in tos or "intransitive" in tos:
            tag.display += "i"
            tag.tooltip = "intransitive " + tag.tooltip
        if "transitive verb" in tos or "transitive" in tos:
            tag.display += "t"
            tag.tooltip = "transitive " + tag.tooltip

        return tag

    def get_sentences(self) -> list[SentenceNote]:
        from ankiutils import app
        return app.col().sentences.with_vocab(self)

    def get_sentences_with_owned_form(self) -> list[SentenceNote]:
        from ankiutils import app
        return app.col().sentences.with_vocab_owned_form(self)

    def get_sentences_with_primary_form(self) -> list[SentenceNote]:
        from ankiutils import app
        return app.col().sentences.with_form(self.get_question())

    def get_user_highlighted_sentences(self) -> list[SentenceNote]:
        from ankiutils import app
        return [sentence for sentence in app.col().sentences.with_highlighted_vocab(self)]

    def get_sentences_studying(self) -> list[SentenceNote]:
        return [sentence for sentence in self.get_sentences() if sentence.is_studying()]

    @staticmethod
    def _get_studying_sentence_count(sentences: list[SentenceNote], card: str = "") -> int:
        return len([sentence for sentence in sentences if sentence.is_studying(card)])

    def get_meta_tags_html(self, display_extended_sentence_statistics: bool = True) -> str:
        tags = set(self.get_tags())
        meta: list[VocabMetaTag] = []
        tos = set([t.lower().strip() for t in self.get_speech_type().split(",")])

        def max_nine_number(value: int) -> str: return f"""{value}""" if value < 10 else "+"
        highlighted_in = self.get_user_highlighted_sentences()
        meta.append(VocabMetaTag("highlighted_in_sentences", f"""{max_nine_number(len(highlighted_in))}""", f"""highlighted in {len(highlighted_in)} sentences"""))

        sentences = self.get_sentences_with_owned_form()
        if sentences:
            studying_sentences_reading = self._get_studying_sentence_count(sentences, NoteFields.VocabNoteType.Card.Reading)
            studying_sentences_listening = self._get_studying_sentence_count(sentences, NoteFields.VocabNoteType.Card.Listening)
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
        if "ichidan verb" in tos: meta.append(self._create_verb_meta_tag("ichidan", "1", "ichidan verb", tos))
        if "godan verb" in tos: meta.append(self._create_verb_meta_tag("godan", "5", "godan verb", tos))
        if "suru verb" in tos or "verbal noun" in tos or "する verb" in tos: meta.append(self._create_verb_meta_tag("suru-verb", "為", "suru verb", tos))
        if "kuru verb" in tos: meta.append(self._create_verb_meta_tag("kuru-verb", "k-v", "kuru verb", tos))
        if "auxiliary verb" in tos: meta.append(self._create_verb_meta_tag("auxiliary-verb", "aux-v", "auxiliary verb", tos))

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

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        super().update_from_wani(wani_vocab)

        self.set_reading_mnemonic(wani_vocab.reading_mnemonic)

        readings = [reading.reading for reading in wani_vocab.readings]
        self._set_reading(", ".join(readings))

        component_subject_ids = [str(subject_id) for subject_id in wani_vocab.component_subject_ids]
        self.set_component_subject_ids(", ".join(component_subject_ids))

        client = WanikaniClient.get_instance()
        kanji_subjects = [client.get_kanji_by_id(int(kanji_id)) for kanji_id in wani_vocab.component_subject_ids]
        kanji_characters = [subject.characters for subject in kanji_subjects]
        self.set_kanji(", ".join(kanji_characters))

    @staticmethod
    def create_from_wani_vocabulary(wani_vocab: models.Vocabulary) -> None:
        from ankiutils import app
        note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        vocab_note = VocabNote(note)
        app.anki_collection().addNote(note)
        vocab_note.set_question(wani_vocab.characters)
        vocab_note.update_from_wani(wani_vocab)

        # Do not move to update method, or we will wipe out local changes made to the context sentences.
        if len(wani_vocab.context_sentences) > 0:
            vocab_note.set_context_en(wani_vocab.context_sentences[0].english)
            vocab_note.set_context_jp(wani_vocab.context_sentences[0].japanese)

        if len(wani_vocab.context_sentences) > 1:
            vocab_note.set_context_en_2(wani_vocab.context_sentences[1].english)
            vocab_note.set_context_jp_2(wani_vocab.context_sentences[1].japanese)

        if len(wani_vocab.context_sentences) > 2:
            vocab_note.set_context_en_3(wani_vocab.context_sentences[2].english)
            vocab_note.set_context_jp_3(wani_vocab.context_sentences[2].japanese)

    def generate_and_set_answer(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        dict_lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if dict_lookup.found_words():
            generated = dict_lookup.entries[0].generate_answer()
            self.set_user_answer(generated)

    def can_generate_sentences_from_context_sentences(self, require_audio: bool) -> bool:
        from ankiutils import app

        def can_create_sentence(question: str, audio: str) -> bool:
            return question != "" and (audio or not require_audio) and not app.col().sentences.with_question(question)

        return ((can_create_sentence(question=self.get_context_jp(), audio=self.get_context_jp_audio()) or
                 can_create_sentence(question=self.get_context_jp_2(), audio=self.get_context_jp_2_audio())) or
                can_create_sentence(question=self.get_context_jp_3(), audio=self.get_context_jp_3_audio()))

    def generate_sentences_from_context_sentences(self, require_audio: bool) -> None:
        from ankiutils import app
        from note.sentencenote import SentenceNote

        def create_sentence_if_not_present(question: str, answer: str, audio: str) -> None:
            if question and (audio or not require_audio) and not app.col().sentences.with_question(question):
                SentenceNote.add_sentence(question=question, answer=answer, audio=audio, highlighted_vocab={self.get_question()})

        create_sentence_if_not_present(question=self.get_context_jp(), answer=self.get_context_en(), audio=self.get_context_jp_audio())
        create_sentence_if_not_present(question=self.get_context_jp_2(), answer=self.get_context_en_2(), audio=self.get_context_jp_2_audio())
        create_sentence_if_not_present(question=self.get_context_jp_3(), answer=self.get_context_en_3(), audio=self.get_context_jp_3_audio())

    @classmethod
    def create_with_dictionary(cls, question: str) -> VocabNote:
        dict_entry = DictLookup.lookup_word_shallow(question)
        if not dict_entry.found_words(): return cls.create(question, "TODO", [])
        readings = list(set(ex_sequence.flatten([ent.kana_forms() for ent in dict_entry.entries])))
        created = cls.create(question, "TODO", readings)
        created.generate_and_set_answer()
        return created

    @classmethod
    def create(cls, question: str, answer: str, readings: list[str]) -> VocabNote:
        from ankiutils import app
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
        note = VocabNote(backend_note)
        note.set_question(question)
        note.set_user_answer(answer)
        note.set_readings(readings)
        note.update_generated_data()
        app.anki_collection().addNote(backend_note)
        return note

    def requires_exact_match(self) -> bool:
        return self.has_tag(Mine.Tags.requires_exact_match)

    def is_ichidan(self) -> bool:
        return "ichidan" in self.get_speech_type().lower()

    def is_godan(self) -> bool:
        return "ichidan" in self.get_speech_type().lower()

    def _get_stems_for_form(self, form: str) -> list[str]:
        return [base for base in language_services.conjugator.get_word_stems(form, is_ichidan_verb=self.is_ichidan()) if base != form]

    def get_stems_for_primary_form(self) -> list[str]:
        return ex_sequence.remove_duplicates_while_retaining_order(self._get_stems_for_form(self.get_question()))

    def get_text_matching_forms_for_primary_form(self) -> list[str]:
        return [self.get_question_without_noise_characters()] + self._get_stems_for_form(self.get_question_without_noise_characters())

    def get_text_matching_forms_for_all_form(self) -> list[str]:
        return [self._strip_noise_characters(form) for form in self.get_forms_list() + self.get_stems_for_all_forms()]

    def get_stems_for_all_forms(self) -> list[str]:
        return ex_sequence.flatten([self._get_stems_for_form(form) for form in self.get_forms()])

    def clone(self) -> VocabNote:
        clone = self.create(self.get_question(), self.get_answer(), self.get_readings())

        for i in range(len(self._note.fields)):
            clone._note.fields[i] = self._note.fields[i]

        for related in clone.get_related_similar_meaning():
            clone.add_related_similar_meaning(related)

        clone._flush()

        return clone

    def is_question_overrides_form(self) -> bool: return self.has_tag(Mine.Tags.question_overrides_form)

    def auto_generate_compounds(self) -> None:
        from ankiutils import app
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        analysis = TextAnalysis(self.get_question(), {WordExclusion(form) for form in self.get_forms()})
        compound_parts = [a.form for a in analysis.display_words if a.form not in self.get_forms()]
        if not len(compound_parts) > 1:#time to brute force it
            word = self.get_question()
            all_substrings = [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1) if word[i:j] != word]
            all_word_substrings = [w for w in all_substrings if DictLookup.is_dictionary_or_collection_word(w)]
            compound_parts = [segment for segment in all_word_substrings if not any(parent for parent in all_word_substrings if segment in parent and parent != segment)]

        segments_missing_vocab = [segment for segment in compound_parts if not app.col().vocab.is_word(segment)]
        for missing in segments_missing_vocab:
            created = VocabNote.create_with_dictionary(missing)
            created.suspend_all_cards()

        self.set_user_compounds(compound_parts)
