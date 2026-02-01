# noinspection PyUnusedName
from __future__ import annotations

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from typed_linq_collections.collections.q_set import QSet


class Builtin(Slots):
    # noinspection PyUnusedName
    Tag: str = "tag"
    Note: str = "note"
    Deck: str = "deck"
    Card: str = "card"

class MyNoteFields(Slots):
    question: str = "Q"
    answer: str = "A"

class ImmersionKitSentenceNoteFields(Slots):
    audio: str = "Audio Sentence"
    id: str = "ID"
    screenshot: str = "Screenshot"
    reading: str = "Reading"
    answer: str = "English"
    question: str = "Expression"

class SentenceNoteFields(Slots):
    reading: str = "Reading"
    id: str = "ID"
    active_question: str = MyNoteFields.question
    source_question: str = "source_question"
    source_comments: str = "Comments"
    user_comments: str = "__comments"
    user_question: str = "__question"
    active_answer: str = MyNoteFields.answer
    source_answer: str = "source_answer"
    user_answer: str = "__answer"
    parsing_result: str = "__parsing_result"
    audio: str = "Audio Sentence"
    screenshot: str = "Screenshot"
    configuration: str = "__configuration"

class CardTypes(Slots):
    reading: str = "Reading"
    listening: str = "Listening"

class NoteTypes(Slots):
    immersion_kit: str = "Immersion Kit Sentence"
    Kanji: str = "_Kanji"
    Vocab: str = "_Vocab"
    Sentence: str = "_japanese_sentence"

    ALL: QSet[str] = QSet((Kanji, Vocab, Sentence))

class NoteFields(Slots):
    note_id: str = "nid"

    class VocabNoteType(Slots):
        class Card(Slots):
            Reading: str = CardTypes.reading
            Listening: str = CardTypes.listening

    class SentencesNoteType(Slots):
        class Card(Slots):
            Reading: str = CardTypes.reading
            Listening: str = CardTypes.listening

    class Kanji(Slots):
        question: str = MyNoteFields.question
        active_answer: str = MyNoteFields.answer
        source_answer: str = "source_answer"
        user_answer: str = "__answer"
        Reading_On: str = "Reading_On"
        Reading_Kun: str = "Reading_Kun"
        Reading_Nan: str = "__reading_Nan"
        Radicals: str = "Radicals"
        Source_Meaning_Mnemonic: str = "Meaning_Mnemonic"
        Meaning_Info: str = "Meaning_Info"
        Reading_Mnemonic: str = "Reading_Mnemonic"
        Reading_Info: str = "Reading_Info"
        PrimaryVocab: str = "__primary_Vocab"
        Audio__: str = "__audio"

        user_mnemonic: str = "__mnemonic"
        user_similar_meaning: str = "__similar_meaning"
        related_confused_with: str = "__confused_with"

    class Vocab(Slots):
        matching_rules: str = "__matching_rules"
        related_vocab: str = "__related_vocab"
        sentence_count: str = "sentence_count"
        question: str = MyNoteFields.question
        active_answer: str = MyNoteFields.answer
        source_answer: str = "source_answer"
        user_answer: str = "__answer"
        user_explanation: str = "__explanation"
        user_explanation_long: str = "__explanation_long"
        user_compounds: str = "__compounds"
        user_mnemonic: str = "__mnemonic"
        Reading: str = "Reading"
        parts_of_speech: str = "TOS"
        source_mnemonic: str = "source_mnemonic"
        Audio_b: str = "Audio_b"
        Audio_g: str = "Audio_g"
        Audio_TTS: str = "Audio_TTS"

        Forms: str = "F"
        source_reading_mnemonic: str = "source_reading_mnemonic"
        Homophones: str = "Homophones"
        ParsedTypeOfSpeech: str = "ParsedTypeOfSpeech"

class Mine(Slots):
    app_name: str = "JA-Studio"
    app_still_loading_message: str = f"{app_name} still loading, the view will refresh when done..."
    VocabPrefixSuffixMarker: str = "〜"
