using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using Compze.Utilities.Logging;
using Wacton.Desu.Japanese;
using NameDictionary = Wacton.Desu.Names.NameDictionary;
using INameEntry = Wacton.Desu.Names.INameEntry;

namespace JAStudio.Core.LanguageServices.JamdictEx;

class DesuDictionary
{
   static readonly object Lock = new();
   static DesuDictionary? _instance;

   public static DesuDictionary GetInstance()
   {
      if(_instance != null) return _instance;
      lock(Lock)
      {
         return _instance ??= new DesuDictionary();
      }
   }

   public static void ShutDown()
   {
      lock(Lock)
      {
         _instance = null;
      }
   }

   readonly Dictionary<string, List<IJapaneseEntry>> _wordsByKanji;
   readonly Dictionary<string, List<IJapaneseEntry>> _wordsByReading;
   readonly Dictionary<string, List<INameEntry>> _namesByKanji;
   readonly Dictionary<string, List<INameEntry>> _namesByReading;
   readonly HashSet<string> _allWordForms;
   readonly HashSet<string> _allNameForms;

   DesuDictionary()
   {
      var stopwatch = Stopwatch.StartNew();
      this.Log().Info("Loading Desu dictionaries...");

      var japaneseEntries = JapaneseDictionary.ParseEntries().ToList();
      _wordsByKanji = new Dictionary<string, List<IJapaneseEntry>>();
      _wordsByReading = new Dictionary<string, List<IJapaneseEntry>>();

      foreach(var entry in japaneseEntries)
      {
         foreach(var kanji in entry.Kanjis)
         {
            if(!_wordsByKanji.TryGetValue(kanji.Text, out var list))
            {
               list = [];
               _wordsByKanji[kanji.Text] = list;
            }

            list.Add(entry);
         }

         foreach(var reading in entry.Readings)
         {
            if(!_wordsByReading.TryGetValue(reading.Text, out var list))
            {
               list = [];
               _wordsByReading[reading.Text] = list;
            }

            list.Add(entry);
         }
      }

      _allWordForms = new HashSet<string>(_wordsByKanji.Keys);
      _allWordForms.UnionWith(_wordsByReading.Keys);

      this.Log().Info($"Loaded {japaneseEntries.Count} Japanese word entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      var nameEntries = NameDictionary.ParseEntries().ToList();
      _namesByKanji = new Dictionary<string, List<INameEntry>>();
      _namesByReading = new Dictionary<string, List<INameEntry>>();

      foreach(var entry in nameEntries)
      {
         foreach(var kanji in entry.Kanjis)
         {
            if(!_namesByKanji.TryGetValue(kanji.Text, out var list))
            {
               list = [];
               _namesByKanji[kanji.Text] = list;
            }

            list.Add(entry);
         }

         foreach(var reading in entry.Readings)
         {
            if(!_namesByReading.TryGetValue(reading.Text, out var list))
            {
               list = [];
               _namesByReading[reading.Text] = list;
            }

            list.Add(entry);
         }
      }

      _allNameForms = new HashSet<string>(_namesByKanji.Keys);
      _allNameForms.UnionWith(_namesByReading.Keys);

      this.Log().Info($"Loaded {nameEntries.Count} name entries in {stopwatch.ElapsedMilliseconds}ms");
   }

   public HashSet<string> AllWordForms => _allWordForms;
   public HashSet<string> AllNameForms => _allNameForms;

   public List<DictEntry> LookupWord(string word)
   {
      var entries = new List<IJapaneseEntry>();

      if(_wordsByKanji.TryGetValue(word, out var kanjiMatches))
         entries.AddRange(kanjiMatches);

      if(_wordsByReading.TryGetValue(word, out var readingMatches))
      {
         foreach(var entry in readingMatches)
         {
            if(!entries.Contains(entry))
               entries.Add(entry);
         }
      }

      return entries.Select(e => DictEntry.FromDesu(e)).ToList();
   }

   public List<DictEntry> LookupName(string word)
   {
      var entries = new List<INameEntry>();

      if(_namesByKanji.TryGetValue(word, out var kanjiMatches))
         entries.AddRange(kanjiMatches);

      if(_namesByReading.TryGetValue(word, out var readingMatches))
      {
         foreach(var entry in readingMatches)
         {
            if(!entries.Contains(entry))
               entries.Add(entry);
         }
      }

      return entries.Select(e => DictEntry.FromDesuName(e)).ToList();
   }
}
