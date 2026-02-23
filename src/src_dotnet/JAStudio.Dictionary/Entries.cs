using System.Collections.Generic;

namespace JAStudio.Dictionary;

public sealed class WordEntry(
   long id,
   IReadOnlyList<WordKanji> kanjis,
   IReadOnlyList<WordReading> readings,
   IReadOnlyList<WordSense> senses)
{
   public long Id { get; } = id;
   public IReadOnlyList<WordKanji> Kanjis { get; } = kanjis;
   public IReadOnlyList<WordReading> Readings { get; } = readings;
   public IReadOnlyList<WordSense> Senses { get; } = senses;
}

public sealed class WordKanji(string text, IReadOnlyList<string> priorities)
{
   public string Text { get; } = text;
   public IReadOnlyList<string> Priorities { get; } = priorities;
}

public sealed class WordReading(string text, IReadOnlyList<string> priorities)
{
   public string Text { get; } = text;
   public IReadOnlyList<string> Priorities { get; } = priorities;
}

public sealed class WordSense(
   IReadOnlyList<string> glosses,
   IReadOnlyList<string> partsOfSpeech,
   IReadOnlyList<string> miscellanea)
{
   public IReadOnlyList<string> Glosses { get; } = glosses;
   public IReadOnlyList<string> PartsOfSpeech { get; } = partsOfSpeech;
   public IReadOnlyList<string> Miscellanea { get; } = miscellanea;
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

public sealed class NameKanji(string text, IReadOnlyList<string> priorities)
{
   public string Text { get; } = text;
   public IReadOnlyList<string> Priorities { get; } = priorities;
}

public sealed class NameReading(string text, IReadOnlyList<string> priorities)
{
   public string Text { get; } = text;
   public IReadOnlyList<string> Priorities { get; } = priorities;
}

public sealed class NameTranslation(IReadOnlyList<string> transcriptions)
{
   public IReadOnlyList<string> Transcriptions { get; } = transcriptions;
}
