using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using JAStudio.Core.SysUtils;
using JAStudio.Core.Note;
using JAStudio.PythonInterop.Utilities;

namespace JAStudio.Core.LanguageServices.JamdictEx;

public static class DictLookup
{
    private static readonly JamdictThreadingWrapper JamdictThreadingWrapper = new();
    
    private static HashSet<string>? _allWordForms;
    private static HashSet<string>? _allNameForms;

    // Cache dictionaries for @cache decorator equivalent
    private static readonly ConcurrentDictionary<(string, string), DictLookupResult> TryLookupWithReadingCache = new();
    private static readonly ConcurrentDictionary<string, List<DictEntry>> LookupWordRawCache = new();
    private static readonly ConcurrentDictionary<string, List<DictEntry>> LookupNameRawCache = new();
    private static readonly ConcurrentDictionary<string, bool> IsWordCache = new();

    private static HashSet<string> FindAllWords()
    {
        var stopwatch = Stopwatch.StartNew();
        MyLog.Info("Prepopulating all word forms from jamdict.");
        
        var kanjiFormsQuery = "SELECT distinct text FROM Kanji";
        var kanaFormsQuery = "SELECT distinct text FROM Kana";
        
        var kanjiForms = JamdictThreadingWrapper.RunStringQuery(kanjiFormsQuery);
        var kanaForms = JamdictThreadingWrapper.RunStringQuery(kanaFormsQuery);
        
        var result = new HashSet<string>(kanjiForms);
        result.UnionWith(kanaForms);
        
        stopwatch.Stop();
        MyLog.Info($"Prepopulating all word forms from jamdict completed in {stopwatch.ElapsedMilliseconds}ms");
        
        return result;
    }

    private static HashSet<string> FindAllNames()
    {
        var stopwatch = Stopwatch.StartNew();
        MyLog.Info("Prepopulating all name forms from jamdict.");
        
        var kanjiFormsQuery = "SELECT distinct text FROM NEKanji";
        var kanaFormsQuery = "SELECT distinct text FROM NEKana";
        
        var kanjiForms = JamdictThreadingWrapper.RunStringQuery(kanjiFormsQuery);
        var kanaForms = JamdictThreadingWrapper.RunStringQuery(kanaFormsQuery);
        
        var result = new HashSet<string>(kanjiForms);
        result.UnionWith(kanaForms);
        
        stopwatch.Stop();
        MyLog.Info($"Prepopulating all name forms from jamdict completed in {stopwatch.ElapsedMilliseconds}ms");
        
        return result;
    }

    private static HashSet<string> AllWordForms()
    {
        if (_allWordForms == null)
        {
            _allWordForms = FindAllWords();
        }
        return _allWordForms;
    }

    private static HashSet<string> AllNameForms()
    {
        if (_allNameForms == null)
        {
            _allNameForms = FindAllNames();
        }
        return _allNameForms;
    }

    public static DictLookupResult LookupVocabWordOrName(VocabNote vocab)
    {
        if (vocab.Readings.Get().Any())
        {
            return LookupWordOrNameWithMatchingReading(
                vocab.Question.WithoutNoiseCharacters, 
                vocab.Readings.Get()
            );
        }

        return LookupWordOrName(vocab.Question.WithoutNoiseCharacters);
    }

    public static DictLookupResult LookupWordOrNameWithMatchingReading(string word, List<string> readings)
    {
        if (readings.Count == 0)
        {
            throw new ArgumentException("readings may not be empty. If you want to match without filtering on reading, use LookupWordOrName instead");
        }
        
        return TryLookupWordOrNameWithMatchingReading(word, readings);
    }

    private static DictLookupResult TryLookupWordOrNameWithMatchingReading(string word, List<string> readings)
    {
        if (!MightBeEntry(word))
        {
            return DictLookupResult.Failed();
        }

        // Create cache key from readings
        var readingsKey = string.Join(",", readings.OrderBy(x => x));
        var cacheKey = (word, readingsKey);

        return TryLookupWithReadingCache.GetOrAdd(cacheKey, _ => 
            TryLookupWordOrNameWithMatchingReadingInner(word, readings));
    }

    private static DictLookupResult TryLookupWordOrNameWithMatchingReadingInner(string word, List<string> readings)
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
        if (!lookup.Any())
        {
            lookup = LookupNameRaw(word);
        }

        var matching = KanaUtils.IsOnlyKana(word) 
            ? AnyKanaOnlyMatches(lookup) 
            : KanjiFormMatches(lookup);

        return new DictLookupResult(matching, word, readings);
    }

    public static DictLookupResult LookupWordOrName(string word)
    {
        if (!MightBeEntry(word))
        {
            return DictLookupResult.Failed();
        }

        var wordHit = LookupWord(word);
        if (wordHit.FoundWords())
        {
            return wordHit;
        }

        return LookupName(word);
    }

    public static DictLookupResult LookupWord(string word)
    {
        if (!MightBeWord(word))
        {
            return DictLookupResult.Failed();
        }

        var entries = LookupWordRaw(word);
        return new DictLookupResult(entries, word, new List<string>());
    }

    public static DictLookupResult LookupName(string word)
    {
        if (!MightBeWord(word))
        {
            return DictLookupResult.Failed();
        }

        var entries = LookupNameRaw(word);
        return new DictLookupResult(entries, word, new List<string>());
    }

    private static List<DictEntry> LookupWordRaw(string word)
    {
        if (!MightBeWord(word))
        {
            return new List<DictEntry>();
        }

        return LookupWordRawCache.GetOrAdd(word, LookupWordRawInner);
    }

    private static List<DictEntry> LookupWordRawInner(string word)
    {
        return PythonEnvironment.Use(() =>
        {
            var lookupResult = JamdictThreadingWrapper.Lookup(word, includeNames: false);
            var entries = new List<dynamic>();
            
            foreach (var entry in Dyn.Enumerate(lookupResult.entries))
            {
                entries.Add(entry);
            }

            List<dynamic> transformed;
            if (!KanaUtils.IsOnlyKana(word))
            {
                transformed = entries;
            }
            else
            {
                transformed = entries.Where(ent => IsKanaOnly(ent)).ToList();
            }

            return DictEntry.Create(transformed);
        });
    }

    private static List<DictEntry> LookupNameRaw(string word)
    {
        if (!MightBeName(word))
        {
            return new List<DictEntry>();
        }

        return LookupNameRawCache.GetOrAdd(word, LookupNameRawInner);
    }

    private static List<DictEntry> LookupNameRawInner(string word)
    {
        return PythonEnvironment.Use(() =>
        {
            var lookupResult = JamdictThreadingWrapper.Lookup(word, includeNames: true);
            var result = new List<dynamic>();
            
            foreach (var name in Dyn.Enumerate(lookupResult.names))
            {
                result.Add(name);
            }

            return DictEntry.Create(result);
        });
    }

    private static bool IsKanaOnly(dynamic entry)
    {
        // Check if no kanji forms
        var hasKanjiForms = false;
        foreach (var _ in Dyn.Enumerate(entry.kanji_forms))
        {
            hasKanjiForms = true;
            break;
        }

        if (!hasKanjiForms)
        {
            return true;
        }

        // Check if any sense has "word usually written using kana alone"
        foreach (var sense in Dyn.Enumerate(entry.senses))
        {
            foreach (var misc in Dyn.Enumerate(sense.misc))
            {
                if ((string)misc == "word usually written using kana alone")
                {
                    return true;
                }
            }
        }

        return false;
    }

    public static bool MightBeWord(string word)
    {
        return App.IsTesting || AllWordForms().Contains(word);
    }

    public static bool MightBeName(string word)
    {
        return App.IsTesting || AllNameForms().Contains(word);
    }

    public static bool MightBeEntry(string word)
    {
        return MightBeWord(word) || MightBeName(word);
    }

    public static bool IsWord(string word)
    {
        if (!MightBeWord(word))
        {
            return false;
        }

        return IsWordCache.GetOrAdd(word, IsWordInner);
    }

    private static bool IsWordInner(string word)
    {
        return LookupWord(word).FoundWords();
    }

    public static bool IsDictionaryOrCollectionWord(string word)
    {
        return App.Col().Vocab.IsWord(word) || IsWord(word);
    }

    public static void EnsureLoadedIntoMemory()
    {
        LookupNameRaw("桜");
        LookupWordRaw("俺");
    }
}
