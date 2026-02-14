using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.Anki;

/// Typed read-only wrapper around a raw Anki note's field dictionary.
/// Encapsulates all knowledge of Anki's field naming conventions for vocab notes.
public class AnkiVocabNote
{
   readonly NoteData _data;

   public AnkiVocabNote(NoteData data) => _data = data;

   public NoteData Raw => _data;
   public NoteId? Id => _data.Id;
   public List<string> Tags => _data.Tags;

   public string Question => Field(AnkiFieldNames.Vocab.Question);
   public string SourceAnswer => Field(AnkiFieldNames.Vocab.SourceAnswer);
   public string UserAnswer => Field(AnkiFieldNames.Vocab.UserAnswer);
   public string ActiveAnswer => Field(AnkiFieldNames.Vocab.ActiveAnswer);
   public string UserExplanation => Field(AnkiFieldNames.Vocab.UserExplanation);
   public string UserExplanationLong => Field(AnkiFieldNames.Vocab.UserExplanationLong);
   public string UserMnemonic => Field(AnkiFieldNames.Vocab.UserMnemonic);
   public string UserCompounds => Field(AnkiFieldNames.Vocab.UserCompounds);
   public string Reading => Field(AnkiFieldNames.Vocab.Reading);
   public string PartsOfSpeech => Field(AnkiFieldNames.Vocab.PartsOfSpeech);
   public string SourceMnemonic => Field(AnkiFieldNames.Vocab.SourceMnemonic);
   public string SourceReadingMnemonic => Field(AnkiFieldNames.Vocab.SourceReadingMnemonic);
   public string AudioB => Field(AnkiFieldNames.Vocab.AudioB);
   public string AudioG => Field(AnkiFieldNames.Vocab.AudioG);
   public string AudioTTS => Field(AnkiFieldNames.Vocab.AudioTTS);
   public string Kanji => Field(AnkiFieldNames.Vocab.Kanji);
   public string Forms => Field(AnkiFieldNames.Vocab.Forms);
   public string SentenceCount => Field(AnkiFieldNames.Vocab.SentenceCount);
   public string MatchingRules => Field(AnkiFieldNames.Vocab.MatchingRules);
   public string RelatedVocab => Field(AnkiFieldNames.Vocab.RelatedVocab);
   public string TechnicalNotes => Field(AnkiFieldNames.Vocab.TechnicalNotes);
   public string References => Field(AnkiFieldNames.Vocab.References);
   public string Image => Field(AnkiFieldNames.Vocab.Image);
   public string UserImage => Field(AnkiFieldNames.Vocab.UserImage);

   string Field(string name) => _data.Fields.TryGetValue(name, out var value) ? value : string.Empty;
}

/// Typed read-only wrapper around a raw Anki note's field dictionary.
/// Encapsulates all knowledge of Anki's field naming conventions for kanji notes.
public class AnkiKanjiNote
{
   readonly NoteData _data;

   public AnkiKanjiNote(NoteData data) => _data = data;

   public NoteData Raw => _data;
   public NoteId? Id => _data.Id;
   public List<string> Tags => _data.Tags;

   public string Question => Field(AnkiFieldNames.Kanji.Question);
   public string SourceAnswer => Field(AnkiFieldNames.Kanji.SourceAnswer);
   public string UserAnswer => Field(AnkiFieldNames.Kanji.UserAnswer);
   public string ActiveAnswer => Field(AnkiFieldNames.Kanji.ActiveAnswer);
   public string ReadingOn => Field(AnkiFieldNames.Kanji.ReadingOn);
   public string ReadingKun => Field(AnkiFieldNames.Kanji.ReadingKun);
   public string ReadingNan => Field(AnkiFieldNames.Kanji.ReadingNan);
   public string Radicals => Field(AnkiFieldNames.Kanji.Radicals);
   public string SourceMeaningMnemonic => Field(AnkiFieldNames.Kanji.SourceMeaningMnemonic);
   public string MeaningInfo => Field(AnkiFieldNames.Kanji.MeaningInfo);
   public string ReadingMnemonic => Field(AnkiFieldNames.Kanji.ReadingMnemonic);
   public string ReadingInfo => Field(AnkiFieldNames.Kanji.ReadingInfo);
   public string PrimaryVocab => Field(AnkiFieldNames.Kanji.PrimaryVocab);
   public string Audio => Field(AnkiFieldNames.Kanji.Audio);
   public string PrimaryReadingsTtsAudio => Field(AnkiFieldNames.Kanji.PrimaryReadingsTtsAudio);
   public string References => Field(AnkiFieldNames.Kanji.References);
   public string UserMnemonic => Field(AnkiFieldNames.Kanji.UserMnemonic);
   public string UserSimilarMeaning => Field(AnkiFieldNames.Kanji.UserSimilarMeaning);
   public string RelatedConfusedWith => Field(AnkiFieldNames.Kanji.RelatedConfusedWith);
   public string Image => Field(AnkiFieldNames.Kanji.Image);

   string Field(string name) => _data.Fields.TryGetValue(name, out var value) ? value : string.Empty;
}

/// Typed read-only wrapper around a raw Anki note's field dictionary.
/// Encapsulates all knowledge of Anki's field naming conventions for sentence notes.
public class AnkiSentenceNote
{
   readonly NoteData _data;

   public AnkiSentenceNote(NoteData data) => _data = data;

   public NoteData Raw => _data;
   public NoteId? Id => _data.Id;
   public List<string> Tags => _data.Tags;

   public string SourceQuestion => Field(AnkiFieldNames.Sentence.SourceQuestion);
   public string UserQuestion => Field(AnkiFieldNames.Sentence.UserQuestion);
   public string ActiveQuestion => Field(AnkiFieldNames.Sentence.ActiveQuestion);
   public string SourceAnswer => Field(AnkiFieldNames.Sentence.SourceAnswer);
   public string UserAnswer => Field(AnkiFieldNames.Sentence.UserAnswer);
   public string ActiveAnswer => Field(AnkiFieldNames.Sentence.ActiveAnswer);
   public string SourceComments => Field(AnkiFieldNames.Sentence.SourceComments);
   public string UserComments => Field(AnkiFieldNames.Sentence.UserComments);
   public string Reading => Field(AnkiFieldNames.Sentence.Reading);
   public string ExternalId => Field(AnkiFieldNames.Sentence.Id);
   public string Audio => Field(AnkiFieldNames.Sentence.Audio);
   public string Screenshot => Field(AnkiFieldNames.Sentence.Screenshot);
   public string ParsingResult => Field(AnkiFieldNames.Sentence.ParsingResult);
   public string JanomeTokens => Field(AnkiFieldNames.Sentence.JanomeTokens);
   public string Configuration => Field(AnkiFieldNames.Sentence.Configuration);

   string Field(string name) => _data.Fields.TryGetValue(name, out var value) ? value : string.Empty;
}
