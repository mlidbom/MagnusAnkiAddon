from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import kana_utils

from ..note_constants import Mine, NoteFields

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

def update_generated_data(self: VocabNote) -> None:
    self.set_field(NoteFields.Vocab.sentence_count, str(len(self.sentences.all())))
    self.set_field(NoteFields.Vocab.active_answer, self.get_answer())

    from language_services.jamdict_ex.dict_lookup import DictLookup

    question = self.get_question_without_noise_characters().strip()
    readings = ",".join(self.readings.get())

    if not readings and kana_utils.is_only_kana(question):
        self.readings.set([question])
        self.set_tag(Mine.Tags.UsuallyKanaOnly)

    if len(self.compound_parts.get()) == 0 and self.parts_of_speech.is_suru_verb_included():
        compounds = [question[:-2], "する"]
        self.compound_parts.set(compounds)

    if self.get_question():
        lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if lookup.is_uk() and not self.has_tag(Mine.Tags.DisableKanaOnly):
            self.set_tag(Mine.Tags.UsuallyKanaOnly)

        if not self.forms.unexcluded_set():
            if lookup.found_words():
                self.forms.set_set(lookup.valid_forms(self.is_uk()))

            if self.get_question() not in self.forms.unexcluded_set():
                self.forms.set_set(self.forms.unexcluded_set() | {self.get_question()})

            if self.is_uk() and self.readings.get()[0] not in self.forms.unexcluded_set():
                self.forms.set_set(self.forms.unexcluded_set() | set(self.readings.get()))

        speech_types = self.parts_of_speech.get() - {'Unknown',
                                                     'Godan verbIchidan verb'  # crap inserted by bug in yomitan
                                                     }
        if len(speech_types) == 0:
            self.parts_of_speech.set_automatically_from_dictionary()
