from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import Mine, NoteFields
from sysutils import kana_utils

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

def update_generated_data(vocab: VocabNote) -> None:
    vocab.set_field(NoteFields.Vocab.sentence_count, str(len(vocab.sentences.all())))
    vocab.set_field(NoteFields.Vocab.active_answer, vocab.get_answer())

    from language_services.jamdict_ex.dict_lookup import DictLookup

    question = vocab.question.without_noise_characters().strip()
    readings = ",".join(vocab.readings.get())

    if not readings and kana_utils.is_only_kana(question):
        vocab.readings.set([question])
        vocab.set_tag(Mine.Tags.UsuallyKanaOnly)

    if len(vocab.compound_parts.get()) == 0 and vocab.parts_of_speech.is_suru_verb_included():
        compounds = [question[:-2], "する"]
        vocab.compound_parts.set(compounds)

    if vocab.get_question():
        if vocab.get_question() not in vocab.forms.all_set():
            vocab.forms.set_set(vocab.forms.all_set() | {vocab.get_question()})

        speech_types = vocab.parts_of_speech.get() - {"Unknown",
                                                      "Godan verbIchidan verb"  # crap inserted by bug in yomitan
                                                      }

        if vocab.readings.get():  # if we don't have a reading, the lookup will be too unreliable
            lookup = DictLookup.lookup_vocab_word_or_name(vocab)
            if lookup.is_uk() and not vocab.has_tag(Mine.Tags.DisableKanaOnly):
                vocab.set_tag(Mine.Tags.UsuallyKanaOnly)

            if not vocab.forms.all_set():
                if lookup.found_words():
                    vocab.forms.set_set(lookup.valid_forms(vocab.parts_of_speech.is_uk()))

                if vocab.parts_of_speech.is_uk() and vocab.readings.get()[0] not in vocab.forms.all_set():
                    vocab.forms.set_set(vocab.forms.all_set() | set(vocab.readings.get()))

            if len(speech_types) == 0:
                vocab.parts_of_speech.set_automatically_from_dictionary()
