using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using Compze.Utilities.SystemCE;
using Compze.Utilities.SystemCE.ThreadingCE.ResourceAccess;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.LanguageServices.JamdictEx;

public class DictLookup
{
   readonly IMonitorCE _monitor = IMonitorCE.WithDefaultTimeout();
   readonly VocabCollection _vocab;
   readonly JapaneseConfig _config;

   internal DictLookup(VocabCollection vocab, JapaneseConfig config)
   {
      _vocab = vocab;
      _config = config;
      _jamdictThreadingWrapper = new JamdictThreadingWrapper(config);
      _allWordForms = new LazyCE<HashSet<string>>(FindAllWords);
      _allNameForms = new LazyCE<HashSet<string>>(FindAllWords);
   }

   readonly JamdictThreadingWrapper _jamdictThreadingWrapper;

   LazyCE<HashSet<string>> _allWordForms { get; }
   LazyCE<HashSet<string>> _allNameForms { get; }

   // Cache dictionaries for @cache decorator equivalent
   static readonly ConcurrentDictionary<(string, string), DictLookupResult> TryLookupWithReadingCache = new();
   static readonly ConcurrentDictionary<string, List<DictEntry>> LookupWordRawCache = new();
   static readonly ConcurrentDictionary<string, List<DictEntry>> LookupNameRawCache = new();
   static readonly ConcurrentDictionary<string, bool> IsWordCache = new();

   HashSet<string> FindAllWords()
   {
      var stopwatch = Stopwatch.StartNew();
      MyLog.Info("Prepopulating all word forms from jamdict.");

      var kanjiFormsQuery = "SELECT distinct text FROM Kanji";
      var kanaFormsQuery = "SELECT distinct text FROM Kana";

      var kanjiForms = _jamdictThreadingWrapper.RunStringQuery(kanjiFormsQuery);
      var kanaForms = _jamdictThreadingWrapper.RunStringQuery(kanaFormsQuery);

      var result = new HashSet<string>(kanjiForms);
      result.UnionWith(kanaForms);

      stopwatch.Stop();
      MyLog.Info($"Prepopulating all word forms from jamdict completed in {stopwatch.ElapsedMilliseconds}ms");

      return result;
   }

   HashSet<string> FindAllNames()
   {
      var stopwatch = Stopwatch.StartNew();
      MyLog.Info("Prepopulating all name forms from jamdict.");

      var kanjiFormsQuery = "SELECT distinct text FROM NEKanji";
      var kanaFormsQuery = "SELECT distinct text FROM NEKana";

      var kanjiForms = _jamdictThreadingWrapper.RunStringQuery(kanjiFormsQuery);
      var kanaForms = _jamdictThreadingWrapper.RunStringQuery(kanaFormsQuery);

      var result = new HashSet<string>(kanjiForms);
      result.UnionWith(kanaForms);

      stopwatch.Stop();
      MyLog.Info($"Prepopulating all name forms from jamdict completed in {stopwatch.ElapsedMilliseconds}ms");

      return result;
   }

   HashSet<string> AllNameForms() => _allNameForms.Value;
   HashSet<string> AllWordForms() => _allNameForms.Value;

   public DictLookupResult LookupVocabWordOrName(VocabNote vocab)
   {
      if(vocab.Readings.Get().Any())
      {
         return LookupWordOrNameWithMatchingReading(
            vocab.Question.WithoutNoiseCharacters,
            vocab.Readings.Get()
         );
      }

      return LookupWordOrName(vocab.Question.WithoutNoiseCharacters);
   }

   public DictLookupResult LookupWordOrNameWithMatchingReading(string word, List<string> readings)
   {
      if(readings.Count == 0)
      {
         throw new ArgumentException("readings may not be empty. If you want to match without filtering on reading, use LookupWordOrName instead");
      }

      return TryLookupWordOrNameWithMatchingReading(word, readings);
   }

   DictLookupResult TryLookupWordOrNameWithMatchingReading(string word, List<string> readings)
   {
      if(!MightBeEntry(word))
      {
         return DictLookupResult.Failed();
      }

      // Create cache key from readings
      var readingsKey = string.Join(",", readings.OrderBy(x => x));
      var cacheKey = (word, readingsKey);

      return TryLookupWithReadingCache.GetOrAdd(cacheKey,
                                                _ =>
                                                   TryLookupWordOrNameWithMatchingReadingInner(word, readings));
   }

   DictLookupResult TryLookupWordOrNameWithMatchingReadingInner(string word, List<string> readings)
   {
      List<DictEntry> KanjiFormMatches(List<DictEntry> lookup)
      {
         return lookup
               .Where(entry => readings.Any(reading => entry.HasMatchingKanaForm(reading)) &&
                               entry.KanjiForms.Any() &&
                               entry.HasMatchingKanjiForm(word))
               .ToList();
      }

      List<DictEntry> AnyKanaOnlyMatches(List<DictEntry> lookup)
      {
         return lookup
               .Where(entry => readings.Any(reading => entry.HasMatchingKanaForm(reading)) &&
                               entry.IsKanaOnly())
               .ToList();
      }

      var lookup = LookupWordRaw(word);
      if(!lookup.Any())
      {
         lookup = LookupNameRaw(word);
      }

      var matching = KanaUtils.IsOnlyKana(word)
                        ? AnyKanaOnlyMatches(lookup)
                        : KanjiFormMatches(lookup);

      return new DictLookupResult(matching, word, readings);
   }

   public DictLookupResult LookupWordOrName(string word)
   {
      if(!MightBeEntry(word))
      {
         return DictLookupResult.Failed();
      }

      var wordHit = LookupWord(word);
      if(wordHit.FoundWords())
      {
         return wordHit;
      }

      return LookupName(word);
   }

   public DictLookupResult LookupWord(string word)
   {
      if(!MightBeWord(word))
      {
         return DictLookupResult.Failed();
      }

      var entries = LookupWordRaw(word);
      return new DictLookupResult(entries, word, new List<string>());
   }

   public DictLookupResult LookupName(string word)
   {
      if(!MightBeWord(word))
      {
         return DictLookupResult.Failed();
      }

      var entries = LookupNameRaw(word);
      return new DictLookupResult(entries, word, new List<string>());
   }

   List<DictEntry> LookupWordRaw(string word)
   {
      if(!MightBeWord(word))
      {
         return new List<DictEntry>();
      }

      return LookupWordRawCache.GetOrAdd(word, LookupWordRawInner);
   }

   List<DictEntry> LookupWordRawInner(string word)
   {
      var lookupResult = _jamdictThreadingWrapper.Lookup(word, includeNames: false);
      var entries = lookupResult.Entries;

      if(!KanaUtils.IsOnlyKana(word))
      {
         return entries;
      }

      return entries.Where(ent => ent.IsKanaOnly()).ToList();
   }

   List<DictEntry> LookupNameRaw(string word)
   {
      if(!MightBeName(word))
      {
         return new List<DictEntry>();
      }

      return LookupNameRawCache.GetOrAdd(word, LookupNameRawInner);
   }

   List<DictEntry> LookupNameRawInner(string word)
   {
      var lookupResult = _jamdictThreadingWrapper.Lookup(word, includeNames: true);
      return lookupResult.Names;
   }

   public bool MightBeWord(string word) => App.IsTesting || AllWordForms().Contains(word);

   public bool MightBeName(string word) => App.IsTesting || AllNameForms().Contains(word);

   public bool MightBeEntry(string word) => MightBeWord(word) || MightBeName(word);

   public bool IsWord(string word)
   {
      if(!MightBeWord(word))
      {
         return false;
      }

      return IsWordCache.GetOrAdd(word, IsWordInner);
   }

   bool IsWordInner(string word) => LookupWord(word).FoundWords();

   public bool IsDictionaryOrCollectionWord(string word) => _vocab.IsWord(word) || IsWord(word);

   public void EnsureLoadedIntoMemory()
   {
      LookupNameRaw("桜");
      LookupWordRaw("俺");
   }
}
