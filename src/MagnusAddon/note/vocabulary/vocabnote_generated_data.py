from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import kana_utils

from ..note_constants import Mine, NoteFields

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote


def update_generated_data(self:VocabNote) -> None:
    self.set_field(NoteFields.Vocab.sentence_count, str(len(self.sentences.all())))
    self.set_field(NoteFields.Vocab.active_answer, self.get_answer())

    from language_services.jamdict_ex.dict_lookup import DictLookup

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