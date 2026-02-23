using System.Collections.Generic;
using LinqToDB.Mapping;

namespace JAStudio.Dictionary;

static class PipeEncoding
{
   public static IReadOnlyList<string> Decode(string raw) => string.IsNullOrEmpty(raw) ? [] : raw.Split('|');

   public static string Encode(IReadOnlyList<string> values) => string.Join("|", values);
}

[Table] sealed class WordEntryRow
{
   [PrimaryKey] public long Id { get; init; }
}

[Table] sealed class WordKanjiRow
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string Text { get; init; } = "";
   [Column] public string PrioritiesRaw { get; init; } = "";

   public IReadOnlyList<string> Priorities => PipeEncoding.Decode(PrioritiesRaw);
}

[Table] sealed class WordReadingRow
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string Text { get; init; } = "";
   [Column] public string PrioritiesRaw { get; init; } = "";

   public IReadOnlyList<string> Priorities => PipeEncoding.Decode(PrioritiesRaw);
}

[Table] sealed class WordSenseRow
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string GlossesRaw { get; init; } = "";
   [Column] public string PartsOfSpeechRaw { get; init; } = "";
   [Column] public string MiscellaneaRaw { get; init; } = "";

   public IReadOnlyList<string> Glosses => PipeEncoding.Decode(GlossesRaw);
   public IReadOnlyList<string> PartsOfSpeech => PipeEncoding.Decode(PartsOfSpeechRaw);
   public IReadOnlyList<string> Miscellanea => PipeEncoding.Decode(MiscellaneaRaw);
}

[Table] sealed class NameEntryRow
{
   [PrimaryKey] public long Id { get; init; }
}

[Table] sealed class NameKanjiRow
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string Text { get; init; } = "";
   [Column] public string PrioritiesRaw { get; init; } = "";

   public IReadOnlyList<string> Priorities => PipeEncoding.Decode(PrioritiesRaw);
}

[Table] sealed class NameReadingRow
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string Text { get; init; } = "";
   [Column] public string PrioritiesRaw { get; init; } = "";

   public IReadOnlyList<string> Priorities => PipeEncoding.Decode(PrioritiesRaw);
}

[Table] sealed class NameTranslationRow
{
   [PrimaryKey, Identity] public long Id { get; init; }
   [Column] public long EntryId { get; init; }
   [Column] public string TranscriptionsRaw { get; init; } = "";

   public IReadOnlyList<string> Transcriptions => PipeEncoding.Decode(TranscriptionsRaw);
}
