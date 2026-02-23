using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using LinqToDB;
using LinqToDB.Data;
using Wacton.Desu.Enums;
using Wacton.Desu.Japanese;
using NameDictionary = Wacton.Desu.Names.NameDictionary;
using INameEntry = Wacton.Desu.Names.INameEntry;

namespace JAStudio.Dictionary;

public static class JMDictDatabaseGenerator
{
   const int SchemaVersion = 1;

   public static void Generate(string dbPath, Action<string>? log = null)
   {
      log ??= _ => {};
      var stopwatch = Stopwatch.StartNew();

      using var db = JMDictDb.Open(dbPath);
      db.Execute("PRAGMA journal_mode = OFF");
      db.Execute("PRAGMA synchronous = OFF");

      CreateSchema(db);

      log("Parsing JMDict word entries...");
      var wordEntries = JapaneseDictionary.ParseEntries().ToList();
      log($"Parsed {wordEntries.Count} word entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      InsertWordEntries(db, wordEntries);
      log($"Inserted word entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      log("Parsing JMnedict name entries...");
      var nameEntries = NameDictionary.ParseEntries().ToList();
      log($"Parsed {nameEntries.Count} name entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      InsertNameEntries(db, nameEntries);
      log($"Inserted name entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      CreateIndexes(db);
      log($"Created indexes in {stopwatch.ElapsedMilliseconds}ms");

      db.Execute($"PRAGMA user_version = {SchemaVersion}");
      db.Execute("VACUUM");
   }

   static void CreateSchema(JMDictDb db)
   {
      db.CreateTable<WordEntryRow>();
      db.CreateTable<WordKanji>();
      db.CreateTable<WordReading>();
      db.CreateTable<WordSense>();
      db.CreateTable<NameEntryRow>();
      db.CreateTable<NameKanji>();
      db.CreateTable<NameReading>();
      db.CreateTable<NameTranslation>();
   }

   static void CreateIndexes(JMDictDb db)
   {
      db.Execute("CREATE INDEX idx_word_kanji_text ON word_kanji(text)");
      db.Execute("CREATE INDEX idx_word_reading_text ON word_reading(text)");
      db.Execute("CREATE INDEX idx_word_kanji_entry ON word_kanji(entry_id)");
      db.Execute("CREATE INDEX idx_word_reading_entry ON word_reading(entry_id)");
      db.Execute("CREATE INDEX idx_word_sense_entry ON word_sense(entry_id)");
      db.Execute("CREATE INDEX idx_name_kanji_text ON name_kanji(text)");
      db.Execute("CREATE INDEX idx_name_reading_text ON name_reading(text)");
      db.Execute("CREATE INDEX idx_name_kanji_entry ON name_kanji(entry_id)");
      db.Execute("CREATE INDEX idx_name_reading_entry ON name_reading(entry_id)");
      db.Execute("CREATE INDEX idx_name_translation_entry ON name_translation(entry_id)");
   }

   static void InsertWordEntries(JMDictDb db, List<IJapaneseEntry> entries)
   {
      using var transaction = db.BeginTransaction();

      long id = 1;
      foreach(var entry in entries)
      {
         db.Insert(new WordEntryRow { Id = id });

         foreach(var kanji in entry.Kanjis)
            db.Insert(new WordKanji { EntryId = id, Text = kanji.Text, PrioritiesRaw = JoinCodes(kanji.Priorities) });

         foreach(var reading in entry.Readings)
            db.Insert(new WordReading { EntryId = id, Text = reading.Text, PrioritiesRaw = JoinCodes(reading.Priorities) });

         IEnumerable<PartOfSpeech> lastPos = [];
         foreach(var sense in entry.Senses)
         {
            var currentPos = sense.PartsOfSpeech.ToList();
            if(currentPos.Count > 0)
               lastPos = currentPos;

            var englishGlosses = sense.Glosses
                                     .Where(g => g.Language.Equals(Language.English))
                                     .Select(g => g.Term)
                                     .ToList();

            if(englishGlosses.Count == 0)
               continue;

            var posToUse = currentPos.Count > 0 ? currentPos : lastPos.ToList();

            db.Insert(new WordSense
            {
               EntryId = id,
               GlossesRaw = string.Join("|", englishGlosses),
               PartsOfSpeechRaw = string.Join("|", posToUse.Select(p => p.Code)),
               MiscellaneaRaw = JoinCodes(sense.Miscellanea),
            });
         }

         id++;
      }

      transaction.Commit();
   }

   static void InsertNameEntries(JMDictDb db, List<INameEntry> entries)
   {
      using var transaction = db.BeginTransaction();

      long id = 1;
      foreach(var entry in entries)
      {
         db.Insert(new NameEntryRow { Id = id });

         foreach(var kanji in entry.Kanjis)
            db.Insert(new NameKanji { EntryId = id, Text = kanji.Text, PrioritiesRaw = JoinCodes(kanji.Priorities) });

         foreach(var reading in entry.Readings)
            db.Insert(new NameReading { EntryId = id, Text = reading.Text, PrioritiesRaw = JoinCodes(reading.Priorities) });

         foreach(var translation in entry.Translations)
            db.Insert(new NameTranslation { EntryId = id, TranscriptionsRaw = string.Join("|", translation.Transcriptions) });

         id++;
      }

      transaction.Commit();
   }

   static string JoinCodes<T>(IEnumerable<T> items) where T : notnull
   {
      var codes = items.Select(item =>
      {
         var codeProp = item.GetType().GetProperty("Code");
         return codeProp?.GetValue(item)?.ToString() ?? item.ToString() ?? "";
      });
      return string.Join("|", codes);
   }
}
