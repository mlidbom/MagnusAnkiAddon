using System.Collections.Generic;

namespace JAStudio.Dictionary;

public sealed class WordEntry(long id, IReadOnlyList<WordKanji> kanjis, IReadOnlyList<WordReading> readings, IReadOnlyList<WordSense> senses)
{
   public long Id { get; } = id;
   public IReadOnlyList<WordKanji> Kanjis { get; } = kanjis;
   public IReadOnlyList<WordReading> Readings { get; } = readings;
   public IReadOnlyList<WordSense> Senses { get; } = senses;
}

public sealed class WordKanji
{
   readonly WordKanjiRow _row;

   internal WordKanji(WordKanjiRow row) => _row = row;

   public WordKanji(string text, IReadOnlyList<string> priorities) => _row = new WordKanjiRow { Text = text, PrioritiesRaw = PipeEncoding.Encode(priorities) };

   public string Text => _row.Text;
   public IReadOnlyList<string> Priorities => _row.Priorities;
}

public sealed class WordReading
{
   readonly WordReadingRow _row;

   internal WordReading(WordReadingRow row) => _row = row;

   public WordReading(string text, IReadOnlyList<string> priorities) => _row = new WordReadingRow { Text = text, PrioritiesRaw = PipeEncoding.Encode(priorities) };

   public string Text => _row.Text;
   public IReadOnlyList<string> Priorities => _row.Priorities;
}

public sealed class WordSense
{
   readonly WordSenseRow _row;

   internal WordSense(WordSenseRow row) => _row = row;

   public WordSense(IReadOnlyList<string> glosses, IReadOnlyList<string> partsOfSpeech, IReadOnlyList<string> miscellanea) =>
      _row = new WordSenseRow
             {
                GlossesRaw = PipeEncoding.Encode(glosses),
                PartsOfSpeechRaw = PipeEncoding.Encode(partsOfSpeech),
                MiscellaneaRaw = PipeEncoding.Encode(miscellanea),
             };

   public IReadOnlyList<string> Glosses => _row.Glosses;
   public IReadOnlyList<string> PartsOfSpeech => _row.PartsOfSpeech;
   public IReadOnlyList<string> Miscellanea => _row.Miscellanea;
}

public sealed class NameEntry(long id, IReadOnlyList<NameKanji> kanjis, IReadOnlyList<NameReading> readings, IReadOnlyList<NameTranslation> translations)
{
   public long Id { get; } = id;
   public IReadOnlyList<NameKanji> Kanjis { get; } = kanjis;
   public IReadOnlyList<NameReading> Readings { get; } = readings;
   public IReadOnlyList<NameTranslation> Translations { get; } = translations;
}

public sealed class NameKanji
{
   readonly NameKanjiRow _row;

   internal NameKanji(NameKanjiRow row) => _row = row;

   public string Text => _row.Text;
   public IReadOnlyList<string> Priorities => _row.Priorities;
}

public sealed class NameReading
{
   readonly NameReadingRow _row;

   internal NameReading(NameReadingRow row) => _row = row;

   public string Text => _row.Text;
   public IReadOnlyList<string> Priorities => _row.Priorities;
}

public sealed class NameTranslation
{
   readonly NameTranslationRow _row;

   internal NameTranslation(NameTranslationRow row) => _row = row;

   public IReadOnlyList<string> Transcriptions => _row.Transcriptions;
}
