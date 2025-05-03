from __future__ import annotations

import re
from typing import Tuple, TYPE_CHECKING

from wanikani_api import models
from anki.notes import Note

from note.jpnote import JPNote
from sysutils.ex_str import newline

if TYPE_CHECKING:
    from note.vocabnote import VocabNote

from note.waninote import WaniNote
from note.note_constants import CardTypes, NoteFields, Mine, NoteTypes
from sysutils import ex_sequence, ex_str, kana_utils
from wanikani.wanikani_api_client import WanikaniClient

class KanjiNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_direct_dependencies(self) -> set[JPNote]:
        return set(self.get_radicals_notes())

    def tag_vocab_readings(self, vocab: VocabNote) -> list[str]:
        def primary_reading(read: str) -> str: return f'<span class="kanjiReadingPrimary">{read}</span>'
        def secondary_reading(read: str) -> str: return f'<span class="kanjiReadingSecondary">{read}</span>'

        primary_readings = self.get_primary_readings()
        secondary_readings = [reading for reading in self.get_readings_clean() if reading not in primary_readings and reading]

        result: list[str] = []

        vocab_form = vocab.get_question()
        for vocab_reading in vocab.get_readings():
            found = False
            for kanji_reading in primary_readings:
                if self.reading_in_vocab_reading(kanji_reading, vocab_reading, vocab_form):
                    result.append(vocab_reading.replace(kanji_reading, primary_reading(kanji_reading)))
                    found = True
                    break

            if not found:
                for kanji_reading in secondary_readings:
                    if self.reading_in_vocab_reading(kanji_reading, vocab_reading, vocab_form):
                        result.append(vocab_reading.replace(kanji_reading, secondary_reading(kanji_reading)))
                        found = True
                        break

                if not found:
                    result.append(vocab_reading)

        return result

    def get_question(self) -> str: return self.get_field(NoteFields.Kanji.question)
    def set_question(self, value: str) -> None: self.set_field(NoteFields.Kanji.question, value)

    def get_answer(self) -> str:
        return self.get_user_answer() or self.get_field(NoteFields.Kanji.source_answer)

    def get_answer_text(self) -> str:
        return ex_str.strip_html_markup(self.get_answer())

    def get_user_answer(self) -> str: return self.get_field(NoteFields.Kanji.user_answer)
    def set_user_answer(self, value: str) -> None: return self.set_field(NoteFields.Kanji.user_answer, value)

    def _set_source_answer(self, value: str) -> None: self.set_field(NoteFields.Kanji.source_answer, value)

    def update_generated_data(self) -> None:
        super().update_generated_data()

        self.set_reading_on(kana_utils.to_hiragana(self.get_reading_on_html()))  # Katakana sneaks in via yomitan etc

        def update_primary_audios() -> None:
            from ankiutils import app
            vocab_we_should_play = ex_sequence.flatten([app.col().vocab.with_question(vocab) for vocab in self.get_primary_vocab()])
            self.set_primary_vocab_audio("".join([vo.get_primary_audio() for vo in vocab_we_should_play]) if vocab_we_should_play else "")

        self.set_field(NoteFields.Kanji.active_answer, self.get_answer())
        update_primary_audios()

    def get_vocab_notes_sorted(self) -> list[VocabNote]:
        from note import vocabnote
        vocab_list = vocabnote.sort_vocab_list_by_studying_status(self.get_vocab_notes(), self.get_primary_vocabs_or_defaults())
        return vocab_list

    def get_vocab_notes(self) -> list[VocabNote]:
        from ankiutils import app
        return app.col().vocab.with_kanji_in_main_form(self)

    def get_user_mnemonic(self) -> str: return self.get_field(NoteFields.Kanji.user_mnemonic)
    def set_user_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Kanji.user_mnemonic, value)

    def get_readings_on(self) -> list[str]: return ex_str.extract_comma_separated_values(ex_str.strip_html_markup(self.get_reading_on_html()))
    def get_reading_on_list_html(self) -> list[str]: return ex_str.extract_comma_separated_values(self.get_reading_on_html())

    def get_readings_kun(self) -> list[str]: return ex_str.extract_comma_separated_values(ex_str.strip_html_markup(self.get_reading_kun_html()))
    def get_reading_kun_list_html(self) -> list[str]: return ex_str.extract_comma_separated_values(self.get_reading_kun_html())

    def get_reading_nan_list_html(self) -> list[str]: return ex_str.extract_comma_separated_values(self.get_reading_nan_html())

    def get_readings_clean(self) -> list[str]:
        return [ex_str.strip_html_markup(reading) for reading in self.get_reading_on_list_html() + self.get_reading_kun_list_html() + self.get_reading_nan_list_html()]

    def get_reading_on_html(self) -> str: return self.get_field(NoteFields.Kanji.Reading_On)
    def set_reading_on(self, value: str) -> None: self.set_field(NoteFields.Kanji.Reading_On, value)

    primary_reading_pattern = re.compile(r'<primary>(.*?)</primary>')

    def get_primary_readings(self) -> list[str]:
        return self.get_primary_readings_on() + self.get_primary_readings_kun() + self.get_primary_readings_nan()

    def get_primary_readings_on(self) -> list[str]:
        return [ex_str.strip_html_markup(reading) for reading in KanjiNote.primary_reading_pattern.findall(self.get_reading_on_html())]

    def get_primary_readings_kun(self) -> list[str]:
        return [ex_str.strip_html_markup(reading) for reading in KanjiNote.primary_reading_pattern.findall(self.get_reading_kun_html())]

    def get_primary_readings_nan(self) -> list[str]:
        return [ex_str.strip_html_markup(reading) for reading in KanjiNote.primary_reading_pattern.findall(self.get_reading_nan_html())]

    def get_reading_kun_html(self) -> str: return self.get_field(NoteFields.Kanji.Reading_Kun)
    def set_reading_kun(self, value: str) -> None: self.set_field(NoteFields.Kanji.Reading_Kun, value)

    def get_reading_nan_html(self) -> str: return self.get_field(NoteFields.Kanji.Reading_Nan)

    def add_primary_on_reading(self, reading: str) -> None:
        self.set_reading_on(ex_str.replace_word(reading, f"<primary>{reading}</primary>", self.get_reading_on_html()))

    def remove_primary_on_reading(self, reading: str) -> None:
        self.set_reading_on(self.get_reading_on_html().replace(f"<primary>{reading}</primary>", reading))

    def add_primary_kun_reading(self, reading: str) -> None:
        self.set_reading_kun(ex_str.replace_word(reading, f"<primary>{reading}</primary>", self.get_reading_kun_html()))

    def remove_primary_kun_reading(self, reading: str) -> None:
        self.set_reading_kun(self.get_reading_kun_html().replace(f"<primary>{reading}</primary>", reading))

    def get_radicals(self) -> list[str]: return [rad for rad in ex_str.extract_comma_separated_values(self.get_field(NoteFields.Kanji.Radicals)) if rad != self.get_question()]
    def _set_radicals(self, value: str) -> None: self.set_field(NoteFields.Kanji.Radicals, value)

    def get_radicals_notes(self) -> list[KanjiNote]:
        from ankiutils import app
        return [kanji_radical for kanji_radical in (app.col().kanji.with_kanji(radical) for radical in self.get_radicals()) if kanji_radical]

    def get_radical_dependencies_names(self) -> list[str]:
        return ex_str.extract_comma_separated_values(
            self.get_radicals_names()) + ex_str.extract_comma_separated_values(
            self.get_radicals_icons_names())

    def get_radicals_names(self) -> str: return self.get_field(NoteFields.Kanji.Radicals_Names)
    def set_radicals_names(self, value: str) -> None: self.set_field(NoteFields.Kanji.Radicals_Names, value)

    def get_radicals_icons_names(self) -> str: return self.get_field(NoteFields.Kanji.Radicals_Icons_Names)
    def set_radicals_icons_names(self, value: str) -> None: self.set_field(NoteFields.Kanji.Radicals_Icons_Names, value)

    def get_active_mnemonic(self) -> str:
        from ankiutils import app
        return self.get_user_mnemonic() if self.get_user_mnemonic() \
            else f"# {self.create_default_mnemonic()}" if app.config().prefer_default_mnemocs_to_source_mnemonics.get_value() \
            else self.get_source_meaning_mnemonic()

    def get_user_similar_meaning(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self.get_field(NoteFields.Kanji.user_similar_meaning)))
    def add_user_similar_meaning(self, new_synonym_question: str, _is_recursive_call: bool = False) -> None:
        near_synonyms_questions = self.get_user_similar_meaning()
        near_synonyms_questions.add(new_synonym_question)

        self.set_field(NoteFields.Kanji.user_similar_meaning, ", ".join(near_synonyms_questions))

        if not _is_recursive_call:
            from ankiutils import app
            new_synonym = app.col().kanji.with_kanji(new_synonym_question)
            if new_synonym:
                new_synonym.add_user_similar_meaning(self.get_question(), _is_recursive_call=True)

    def get_source_meaning_mnemonic(self) -> str: return self.get_field(NoteFields.Kanji.Source_Meaning_Mnemonic)
    def set_source_meaning_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Kanji.Source_Meaning_Mnemonic, value)

    def get_related_confused_with(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self.get_field(NoteFields.Kanji.related_confused_with)))
    def add_related_confused_with(self, new_confused_with: str) -> None:
        confused_with = self.get_related_confused_with()
        confused_with.add(new_confused_with)
        self.set_field(NoteFields.Kanji.related_confused_with, ", ".join(confused_with))

    def set_meaning_hint(self, value: str) -> None: self.set_field(NoteFields.Kanji.Meaning_Info, value if value is not None else "")
    def set_reading_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Kanji.Reading_Mnemonic, value)
    def set_reading_hint(self, value: str) -> None: self.set_field(NoteFields.Kanji.Reading_Info, value if value is not None else "")
    def set_amalgamation_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Kanji.amalgamation_subject_ids, value)
    def set_component_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Kanji.component_subject_ids, value)
    def set_vocabs(self, value: str) -> None: self.set_field(NoteFields.Kanji.Vocabs, value)
    def get_primary_vocabs_or_defaults(self) -> list[str]: return self.get_primary_vocab() if self.get_primary_vocab() else self.generate_default_primary_vocab()

    def get_primary_vocab(self) -> list[str]: return ex_str.extract_comma_separated_values(self.get_field(NoteFields.Kanji.PrimaryVocab))
    def set_primary_vocab(self, value: list[str]) -> None: self.set_field(NoteFields.Kanji.PrimaryVocab, ", ".join(value))

    _any_word_pattern = re.compile(r'\b[-\w]+\b', re.UNICODE)
    def get_primary_meaning(self) -> str:
        radical_meaning_match = self._any_word_pattern.search(self.get_answer_text())
        # noinspection PyArgumentEqualDefault
        return radical_meaning_match.group(0) if radical_meaning_match else ""

    _parenthesized_word_pattern = re.compile(r'\([-\w]+\)', re.UNICODE)
    def get_primary_radical_meaning(self) -> str:
        def get_dedicated_radical_primary_meaning() -> str:
            radical_meaning_match = self._parenthesized_word_pattern.search(self.get_answer_text())
            # noinspection PyArgumentEqualDefault
            return radical_meaning_match.group(0).replace("(", "").replace(")", "") if radical_meaning_match else ""

        result = get_dedicated_radical_primary_meaning()
        return result or self.get_primary_meaning()

    def reading_in_vocab_reading(self, kanji_reading: str, vocab_reading: str, vocab_form: str) -> bool:
        vocab_form = ex_str.strip_html_and_bracket_markup_and_noise_characters(vocab_form)
        covering_readings = [covering_reading for covering_reading in self.get_readings_clean() if kanji_reading != covering_reading and kanji_reading in covering_reading]

        if any(covering_reading for covering_reading in covering_readings if self.reading_in_vocab_reading(covering_reading, vocab_reading, vocab_form)):
            return False

        if vocab_form.startswith(self.get_question()):
            return vocab_reading.startswith(kanji_reading)
        elif vocab_form.endswith(self.get_question()):
            return vocab_reading.endswith(kanji_reading)
        else:
            return kanji_reading in vocab_reading[1:-1]

    def generate_default_primary_vocab(self) -> list[str]:
        result: list[str] = []

        def sort_key(_vocab: VocabNote) -> Tuple[int, int]:
            return -len(_vocab.get_sentences_studying()), len(_vocab.get_question())

        studying_reading_vocab_in_descending_studying_sentences_order = sorted((voc for voc in self.get_vocab_notes() if voc.is_studying(CardTypes.reading)), key=sort_key)

        primary_readings = ex_sequence.remove_duplicates_while_retaining_order(self.get_primary_readings())
        for primary_reading in primary_readings:
            for vocab in studying_reading_vocab_in_descending_studying_sentences_order:
                if any(vocab.get_readings()) and self.reading_in_vocab_reading(primary_reading, vocab.get_readings()[0], vocab.get_question()):
                    result.append(vocab.get_question())
                    break

        return result

    def position_primary_vocab(self, vocab: str, new_index: int = -1) -> None:
        vocab = vocab.strip()
        primary_vocab_list = self.get_primary_vocab()
        if vocab in primary_vocab_list:
            primary_vocab_list.remove(vocab)

        if new_index == -1:
            primary_vocab_list.append(vocab)
        else:
            primary_vocab_list.insert(new_index, vocab)

        self.set_primary_vocab(primary_vocab_list)

    def remove_primary_vocab(self, vocab: str) -> None:
        self.set_primary_vocab([v for v in self.get_primary_vocab() if not v == vocab])

    def set_primary_vocab_audio(self, value: str) -> None: self.set_field(NoteFields.Kanji.Audio__, value)

    def bootstrap_mnemonic_from_radicals(self) -> None:
        self.set_user_mnemonic(self.create_default_mnemonic())

    def create_default_mnemonic(self) -> str:
        from ankiutils import app
        readings_mappings = app.config().readings_mappings_dict

        def create_readings_tag(kana_reading: str) -> str:
            romaji_reading = kana_utils.romanize(kana_reading)

            if romaji_reading in readings_mappings:
                return readings_mappings[romaji_reading]

            def try_combine_framentary_matches_into_one_reading() -> str:
                matches_by_reading_character_index: list[list[str]] = list()
                for index in range(0, len(kana_reading)):
                    candidates = [kana_reading[index:sub_index] for sub_index in range(index + 1, len(kana_reading) + 1)]
                    matches_by_reading_character_index.append([cand for cand in candidates if kana_utils.romanize(cand) in readings_mappings])

                def remove_dead_end_paths() -> None:
                    values_removed = True
                    while values_removed:
                        values_removed = False
                        for path_index in range(0, len(kana_reading)):
                            for kana_match in matches_by_reading_character_index[path_index]:
                                if not path_index + len(kana_match) == len(kana_reading):
                                    if not matches_by_reading_character_index[path_index + len(kana_match)]:
                                        values_removed = True
                                        matches_by_reading_character_index[path_index].remove(kana_match)

                def find_long_path() -> list[str]:
                    next_fragment_index = 0
                    path: list[str] = []
                    while next_fragment_index < len(kana_reading):
                        candidates_ = matches_by_reading_character_index[next_fragment_index]
                        if not candidates_:
                            return []

                        fragment = sorted(candidates_, key=lambda x: len(x), reverse=True)[0]
                        path.append(fragment)
                        next_fragment_index += len(fragment)
                    return path

                remove_dead_end_paths()
                long_path = find_long_path()

                if not long_path: return ""
                combined_reading = "-".join([readings_mappings[kana_utils.romanize(fragment)] for fragment in long_path])
                return f"""<compound-reading>{combined_reading}</compound-reading>"""


            combined = try_combine_framentary_matches_into_one_reading()
            if combined: return combined

            return f"<read>{romaji_reading.capitalize()}</read>"

        radical_names = [rad.get_primary_radical_meaning() for rad in self.get_radicals_notes()]
        mnemonic = f"""
{" ".join([f"<rad>{name}</rad>" for name in radical_names])} 
<kan>{self.get_primary_meaning()}</kan> 
{" ".join([create_readings_tag(reading) for reading in self.get_primary_readings()])}
""".replace(newline, "")
        return mnemonic.strip()

    def update_from_wani(self, wani_kanji: models.Kanji) -> None:
        super().update_from_wani(wani_kanji)

        self.set_source_meaning_mnemonic(wani_kanji.meaning_mnemonic)
        self.set_meaning_hint(wani_kanji.meaning_hint)

        self.set_reading_mnemonic(wani_kanji.reading_mnemonic)
        self.set_reading_hint(wani_kanji.reading_hint)

        meanings = [f"<primary>{meaning.meaning}</primary>" if meaning.primary else meaning.meaning
                    for meaning in wani_kanji.meanings]

        self._set_source_answer(", ".join(meanings))

        onyomi_readings = [f"<primary>{reading.reading}</primary>" if reading.primary else reading.reading
                           for reading in wani_kanji.readings if reading.type == "onyomi"]

        kunyomi_readings = [f"<primary>{reading.reading}</primary>" if reading.primary else reading.reading
                            for reading in wani_kanji.readings if reading.type == "kunyomi"]

        self.set_reading_on(", ".join(onyomi_readings))
        self.set_reading_kun(", ".join(kunyomi_readings))

        amalgamation_subject_ids = [str(subject_id) for subject_id in wani_kanji.amalgamation_subject_ids]
        self.set_amalgamation_subject_ids(", ".join(amalgamation_subject_ids))

        component_subject_ids = [str(subject_id) for subject_id in wani_kanji.component_subject_ids]
        self.set_component_subject_ids(", ".join(component_subject_ids))

        client = WanikaniClient.get_instance()
        radicals = [client.get_radical_by_id(int(radical_id)) for radical_id in component_subject_ids]
        radicals_with_characters = [radical for radical in radicals if radical.characters is not None]
        radicals_without_characters = [radical for radical in radicals if radical.characters is None]

        radical_characters = [radical.characters for radical in radicals_with_characters]
        self._set_radicals(", ".join(radical_characters))

        radical_names = [radical.meanings[0].meaning for radical in radicals_with_characters]
        self.set_radicals_names(", ".join(radical_names))

        characterless_radical_names = [radical.meanings[0].meaning for radical in radicals_without_characters]
        self.set_radicals_icons_names(", ".join(characterless_radical_names))

        vocabs = [client.get_vocab_by_id(int(kanji_id)) for kanji_id in amalgamation_subject_ids]
        vocabs.sort(key=lambda voc: (voc.level, voc.lesson_position))
        vocab_html = '''
<div class="vocabList">
    <div>'''

        for vocab in vocabs:
            vocab_html += '''
        <div>{} ({}) {}</div>'''.format(vocab.characters, vocab.readings[0].reading, vocab.meanings[0].meaning)

        vocab_html += '''
    </div>
</div>
'''
        self.set_vocabs(vocab_html)

    def populate_radicals_from_mnemonic_tags(self) -> None:
        def detect_radicals_from_mnemonic() -> list[str]:
            radical_names = re.findall(r'<rad>(.*?)</rad>', self.get_user_mnemonic())

            from ankiutils import app
            matching_radicals = ex_sequence.flatten([([rad for rad in app.col().kanji.all() if re.search(r'\b' + re.escape(radical_name) + r'\b', rad.get_answer())]) for radical_name in radical_names])
            return [match.get_question() for match in matching_radicals]

        radicals = self.get_radicals()
        for radical in detect_radicals_from_mnemonic():
            if radical not in radicals:
                radicals += radical

        self._set_radicals(", ".join(radicals))

    @staticmethod
    def create_from_wani_kanji(wani_kanji: models.Kanji) -> None:
        from ankiutils import app
        note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Kanji))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        kanji_note = KanjiNote(note)
        app.anki_collection().addNote(note)
        kanji_note.set_question(wani_kanji.characters)
        kanji_note.update_from_wani(wani_kanji)

    @classmethod
    def create(cls, question: str, answer: str, on_readings: str, kun_reading: str) -> KanjiNote:
        from ankiutils import app
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Kanji))
        note = KanjiNote(backend_note)
        note.set_question(question)
        note.set_user_answer(answer)
        note.set_reading_on(on_readings)
        note.set_reading_kun(kun_reading)
        note.update_generated_data()
        app.anki_collection().addNote(backend_note)
        return note
