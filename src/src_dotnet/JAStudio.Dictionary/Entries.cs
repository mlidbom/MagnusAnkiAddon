using System.Collections.Generic;

namespace JAStudio.Dictionary;

public sealed record WordEntry(
   long Id,
   IReadOnlyList<WordKanji> Kanjis,
   IReadOnlyList<WordReading> Readings,
   IReadOnlyList<WordSense> Senses);

public sealed record WordKanji(string Text, IReadOnlyList<string> Priorities);

public sealed record WordReading(string Text, IReadOnlyList<string> Priorities);

public sealed record WordSense(
   IReadOnlyList<string> Glosses,
   IReadOnlyList<string> PartsOfSpeech,
   IReadOnlyList<string> Miscellanea);

public sealed record NameEntry(
   long Id,
   IReadOnlyList<NameKanji> Kanjis,
   IReadOnlyList<NameReading> Readings,
   IReadOnlyList<NameTranslation> Translations);

public sealed record NameKanji(string Text, IReadOnlyList<string> Priorities);

public sealed record NameReading(string Text, IReadOnlyList<string> Priorities);

public sealed record NameTranslation(IReadOnlyList<string> Transcriptions);
