using System.Collections.Generic;

namespace JAStudio.Core.Note;

public static class MyNoteFields
{
    public const string Question = "Q";
    public const string Answer = "A";
}

public static class ImmersionKitSentenceNoteFields
{
    public const string Audio = "Audio Sentence";
    public const string Id = "ID";
    public const string Screenshot = "Screenshot";
    public const string Reading = "Reading";
    public const string Answer = "English";
    public const string Question = "Expression";
}

public static class SentenceNoteFields
{
    public const string Reading = "Reading";
    public const string Id = "ID";
    public const string ActiveQuestion = MyNoteFields.Question;
    public const string SourceQuestion = "source_question";
    public const string SourceComments = "Comments";
    public const string UserComments = "__comments";
    public const string UserQuestion = "__question";
    public const string ActiveAnswer = MyNoteFields.Answer;
    public const string SourceAnswer = "source_answer";
    public const string UserAnswer = "__answer";
    public const string ParsingResult = "__parsing_result";
    public const string Audio = "Audio Sentence";
    public const string Screenshot = "Screenshot";
    public const string Configuration = "__configuration";
}

public static class CardTypes
{
    public const string Reading = "Reading";
    public const string Listening = "Listening";
}

public static class NoteTypes
{
    public const string ImmersionKit = "Immersion Kit Sentence";
    public const string Kanji = "_Kanji";
    public const string Vocab = "_Vocab";
    public const string Sentence = "_japanese_sentence";

    public static readonly HashSet<string> All = new() { Kanji, Vocab, Sentence };
}

public static class NoteFields
{
    public const string NoteId = "nid";

    public static class VocabNoteType
    {
        public static class Card
        {
            public const string Reading = CardTypes.Reading;
            public const string Listening = CardTypes.Listening;
        }
    }

    public static class SentencesNoteType
    {
        public static class Card
        {
            public const string Reading = CardTypes.Reading;
            public const string Listening = CardTypes.Listening;
        }
    }

    public static class Kanji
    {
        public const string Question = MyNoteFields.Question;
        public const string ActiveAnswer = MyNoteFields.Answer;
        public const string SourceAnswer = "source_answer";
        public const string UserAnswer = "__answer";
        public const string ReadingOn = "Reading_On";
        public const string ReadingKun = "Reading_Kun";
        public const string ReadingNan = "__reading_Nan";
        public const string Radicals = "Radicals";
        public const string SourceMeaningMnemonic = "Meaning_Mnemonic";
        public const string MeaningInfo = "Meaning_Info";
        public const string ReadingMnemonic = "Reading_Mnemonic";
        public const string ReadingInfo = "Reading_Info";
        public const string PrimaryVocab = "__primary_Vocab";
        public const string Audio = "__audio";
        public const string UserMnemonic = "__mnemonic";
        public const string UserSimilarMeaning = "__similar_meaning";
        public const string RelatedConfusedWith = "__confused_with";
    }

    public static class Vocab
    {
        public const string MatchingRules = "__matching_rules";
        public const string RelatedVocab = "__related_vocab";
        public const string SentenceCount = "sentence_count";
        public const string Question = MyNoteFields.Question;
        public const string ActiveAnswer = MyNoteFields.Answer;
        public const string SourceAnswer = "source_answer";
        public const string UserAnswer = "__answer";
        public const string ReadingKana = "Reading_Kana";
        public const string ReadingRomaji = "Reading_Romaji";
        public const string PartsOfSpeech = "__parts_of_speech";
        public const string Audio = "__audio";
        public const string Kanji = "__kanji";
        public const string UserCompoundParts = "__userCompoundParts";
        public const string UserForms = "__user_forms";
        public const string Register = "__register";
        public const string Metadata = "__metadata";
        public const string MetaTags = "__meta_tags";
        public const string GeneratedData = "__generated_data";
    }
}

public static class Builtin
{
    public const string Tag = "tag";
    public const string Note = "note";
    public const string Deck = "deck";
    public const string Card = "card";
}
