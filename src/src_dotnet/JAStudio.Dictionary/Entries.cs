using System;
using System.Collections.Generic;
using LinqToDB.Mapping;

namespace JAStudio.Dictionary;

// ── Aggregate types (not table-mapped) ──────────────────────────────────────

public sealed class WordEntry(long id,IReadOnlyList<WordKanji> kanjis,IReadOnlyList<WordReading> readings,IReadOnlyList<WordSense> senses)
{
   public long Id { get; } = id;
   public IReadOnlyList<WordKanji> Kanjis { get; } = kanjis;
   public IReadOnlyList<WordReading> Readings { get; } = readings;
   public IReadOnlyList<WordSense> Senses { get; } = senses;
}

public sealed class NameEntry(
   long id,
   IReadOnlyList<NameKanji> kanjis,
   IReadOnlyList<NameReading> readings,
   IReadOnlyList<NameTranslation> translations)
{
   public long Id { get; } = id;
   public IReadOnlyList<NameKanji> Kanjis { get; } = kanjis;
   public IReadOnlyList<NameReading> Readings { get; } = readings;
   public IReadOnlyList<NameTranslation> Translations { get; } = translations;
}

// ── Table-mapped types ──────────────────────────────────────────────────────

static class PipeEncoding
{
   public static IReadOnlyList<string> Decode(string raw) =>
      string.IsNullOrEmpty(raw) ? [] : raw.Split('|');

   public static string Encode(IReadOnlyList<string> values) =>
      string.Join("|", values);
}

[Table]
public sealed class WordEntryRow
{
   [PrimaryKey] public long Id { get; init; }
}

[Table]
public sealed class WordKanji
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string Text { get; init; } = "";
   [Column] public string PrioritiesRaw { get; init; } = "";

   [NotColumn] public IReadOnlyList<string> Priorities => PipeEncoding.Decode(PrioritiesRaw);

   public WordKanji() {}
   public WordKanji(string text, IReadOnlyList<string> priorities)
   {
      Text = text;
      PrioritiesRaw = PipeEncoding.Encode(priorities);
   }
}

[Table]
public sealed class WordReading
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string Text { get; init; } = "";
   [Column] public string PrioritiesRaw { get; init; } = "";

   [NotColumn] public IReadOnlyList<string> Priorities => PipeEncoding.Decode(PrioritiesRaw);

   public WordReading() {}
   public WordReading(string text, IReadOnlyList<string> priorities)
   {
      Text = text;
      PrioritiesRaw = PipeEncoding.Encode(priorities);
   }
}

[Table]
public sealed class WordSense
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string GlossesRaw { get; init; } = "";
   [Column] public string PartsOfSpeechRaw { get; init; } = "";
   [Column] public string MiscellaneaRaw { get; init; } = "";

   [NotColumn] public IReadOnlyList<string> Glosses => PipeEncoding.Decode(GlossesRaw);
   [NotColumn] public IReadOnlyList<string> PartsOfSpeech => PipeEncoding.Decode(PartsOfSpeechRaw);
   [NotColumn] public IReadOnlyList<string> Miscellanea => PipeEncoding.Decode(MiscellaneaRaw);

   public WordSense() {}
   public WordSense(IReadOnlyList<string> glosses, IReadOnlyList<string> partsOfSpeech, IReadOnlyList<string> miscellanea)
   {
      GlossesRaw = PipeEncoding.Encode(glosses);
      PartsOfSpeechRaw = PipeEncoding.Encode(partsOfSpeech);
      MiscellaneaRaw = PipeEncoding.Encode(miscellanea);
   }
}

[Table]
public sealed class NameEntryRow
{
   [PrimaryKey] public long Id { get; init; }
}

[Table]
public sealed class NameKanji
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string Text { get; init; } = "";
   [Column] public string PrioritiesRaw { get; init; } = "";

   [NotColumn] public IReadOnlyList<string> Priorities => PipeEncoding.Decode(PrioritiesRaw);

   public NameKanji() {}
   public NameKanji(string text, IReadOnlyList<string> priorities)
   {
      Text = text;
      PrioritiesRaw = PipeEncoding.Encode(priorities);
   }
}

[Table]
public sealed class NameReading
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string Text { get; init; } = "";
   [Column] public string PrioritiesRaw { get; init; } = "";

   [NotColumn] public IReadOnlyList<string> Priorities => PipeEncoding.Decode(PrioritiesRaw);

   public NameReading() {}
   public NameReading(string text, IReadOnlyList<string> priorities)
   {
      Text = text;
      PrioritiesRaw = PipeEncoding.Encode(priorities);
   }
}

[Table]
public sealed class NameTranslation
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string TranscriptionsRaw { get; init; } = "";

   [NotColumn] public IReadOnlyList<string> Transcriptions => PipeEncoding.Decode(TranscriptionsRaw);

   public NameTranslation() {}
   public NameTranslation(IReadOnlyList<string> transcriptions) =>
      TranscriptionsRaw = PipeEncoding.Encode(transcriptions);
}
