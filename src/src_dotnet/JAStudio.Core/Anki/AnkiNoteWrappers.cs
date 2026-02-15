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
   public string ActiveAnswer => Field(AnkiFieldNames.Vocab.ActiveAnswer);
   public string AudioB => Field(AnkiFieldNames.Vocab.AudioB);
   public string AudioG => Field(AnkiFieldNames.Vocab.AudioG);
   public string AudioTTS => Field(AnkiFieldNames.Vocab.AudioTTS);
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
   public string ActiveAnswer => Field(AnkiFieldNames.Kanji.ActiveAnswer);
   public string Audio => Field(AnkiFieldNames.Kanji.Audio);
   public string PrimaryReadingsTtsAudio => Field(AnkiFieldNames.Kanji.PrimaryReadingsTtsAudio);
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
   public string SourceAnswer => Field(AnkiFieldNames.Sentence.SourceAnswer);
   public string SourceComments => Field(AnkiFieldNames.Sentence.SourceComments);
   public string Reading => Field(AnkiFieldNames.Sentence.Reading);
   public string ExternalId => Field(AnkiFieldNames.Sentence.Id);
   public string Audio => Field(AnkiFieldNames.Sentence.Audio);
   public string Screenshot => Field(AnkiFieldNames.Sentence.Screenshot);

   string Field(string name) => _data.Fields.TryGetValue(name, out var value) ? value : string.Empty;
}
