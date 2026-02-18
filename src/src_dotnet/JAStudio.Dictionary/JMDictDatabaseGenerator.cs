using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using Microsoft.Data.Sqlite;
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

      using var connection = new SqliteConnection($"Data Source={dbPath}");
      connection.Open();

      CreateSchema(connection);

      log("Parsing JMDict word entries...");
      var wordEntries = JapaneseDictionary.ParseEntries().ToList();
      log($"Parsed {wordEntries.Count} word entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      InsertWordEntries(connection, wordEntries);
      log($"Inserted word entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      log("Parsing JMnedict name entries...");
      var nameEntries = NameDictionary.ParseEntries().ToList();
      log($"Parsed {nameEntries.Count} name entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      InsertNameEntries(connection, nameEntries);
      log($"Inserted name entries in {stopwatch.ElapsedMilliseconds}ms");

      stopwatch.Restart();
      CreateIndexes(connection);
      log($"Created indexes in {stopwatch.ElapsedMilliseconds}ms");

      Execute(connection, $"PRAGMA user_version = {SchemaVersion}");
      Execute(connection, "VACUUM");
   }

   static void CreateSchema(SqliteConnection connection)
   {
      Execute(connection, "PRAGMA journal_mode = OFF");
      Execute(connection, "PRAGMA synchronous = OFF");

      Execute(connection, """
         CREATE TABLE word_entry (
            id INTEGER PRIMARY KEY
         )
      """);

      Execute(connection, """
         CREATE TABLE word_kanji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL REFERENCES word_entry(id),
            text TEXT NOT NULL,
            priorities TEXT NOT NULL DEFAULT ''
         )
      """);

      Execute(connection, """
         CREATE TABLE word_reading (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL REFERENCES word_entry(id),
            text TEXT NOT NULL,
            priorities TEXT NOT NULL DEFAULT ''
         )
      """);

      Execute(connection, """
         CREATE TABLE word_sense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL REFERENCES word_entry(id),
            glosses TEXT NOT NULL DEFAULT '',
            pos TEXT NOT NULL DEFAULT '',
            misc TEXT NOT NULL DEFAULT ''
         )
      """);

      Execute(connection, """
         CREATE TABLE name_entry (
            id INTEGER PRIMARY KEY
         )
      """);

      Execute(connection, """
         CREATE TABLE name_kanji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL REFERENCES name_entry(id),
            text TEXT NOT NULL,
            priorities TEXT NOT NULL DEFAULT ''
         )
      """);

      Execute(connection, """
         CREATE TABLE name_reading (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL REFERENCES name_entry(id),
            text TEXT NOT NULL,
            priorities TEXT NOT NULL DEFAULT ''
         )
      """);

      Execute(connection, """
         CREATE TABLE name_translation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL REFERENCES name_entry(id),
            transcriptions TEXT NOT NULL DEFAULT ''
         )
      """);
   }

   static void CreateIndexes(SqliteConnection connection)
   {
      Execute(connection, "CREATE INDEX idx_word_kanji_text ON word_kanji(text)");
      Execute(connection, "CREATE INDEX idx_word_reading_text ON word_reading(text)");
      Execute(connection, "CREATE INDEX idx_word_kanji_entry ON word_kanji(entry_id)");
      Execute(connection, "CREATE INDEX idx_word_reading_entry ON word_reading(entry_id)");
      Execute(connection, "CREATE INDEX idx_word_sense_entry ON word_sense(entry_id)");
      Execute(connection, "CREATE INDEX idx_name_kanji_text ON name_kanji(text)");
      Execute(connection, "CREATE INDEX idx_name_reading_text ON name_reading(text)");
      Execute(connection, "CREATE INDEX idx_name_kanji_entry ON name_kanji(entry_id)");
      Execute(connection, "CREATE INDEX idx_name_reading_entry ON name_reading(entry_id)");
      Execute(connection, "CREATE INDEX idx_name_translation_entry ON name_translation(entry_id)");
   }

   static void InsertWordEntries(SqliteConnection connection, List<IJapaneseEntry> entries)
   {
      using var transaction = connection.BeginTransaction();

      using var entryCmd = connection.CreateCommand();
      entryCmd.CommandText = "INSERT INTO word_entry (id) VALUES ($id)";
      var entryIdParam = entryCmd.Parameters.Add("$id", SqliteType.Integer);

      using var kanjiCmd = connection.CreateCommand();
      kanjiCmd.CommandText = "INSERT INTO word_kanji (entry_id, text, priorities) VALUES ($eid, $text, $pri)";
      var kanjiEidParam = kanjiCmd.Parameters.Add("$eid", SqliteType.Integer);
      var kanjiTextParam = kanjiCmd.Parameters.Add("$text", SqliteType.Text);
      var kanjiPriParam = kanjiCmd.Parameters.Add("$pri", SqliteType.Text);

      using var readingCmd = connection.CreateCommand();
      readingCmd.CommandText = "INSERT INTO word_reading (entry_id, text, priorities) VALUES ($eid, $text, $pri)";
      var readingEidParam = readingCmd.Parameters.Add("$eid", SqliteType.Integer);
      var readingTextParam = readingCmd.Parameters.Add("$text", SqliteType.Text);
      var readingPriParam = readingCmd.Parameters.Add("$pri", SqliteType.Text);

      using var senseCmd = connection.CreateCommand();
      senseCmd.CommandText = "INSERT INTO word_sense (entry_id, glosses, pos, misc) VALUES ($eid, $glosses, $pos, $misc)";
      var senseEidParam = senseCmd.Parameters.Add("$eid", SqliteType.Integer);
      var senseGlossesParam = senseCmd.Parameters.Add("$glosses", SqliteType.Text);
      var sensePosParam = senseCmd.Parameters.Add("$pos", SqliteType.Text);
      var senseMiscParam = senseCmd.Parameters.Add("$misc", SqliteType.Text);

      long id = 1;
      foreach(var entry in entries)
      {
         entryIdParam.Value = id;
         entryCmd.ExecuteNonQuery();

         foreach(var kanji in entry.Kanjis)
         {
            kanjiEidParam.Value = id;
            kanjiTextParam.Value = kanji.Text;
            kanjiPriParam.Value = JoinCodes(kanji.Priorities);
            kanjiCmd.ExecuteNonQuery();
         }

         foreach(var reading in entry.Readings)
         {
            readingEidParam.Value = id;
            readingTextParam.Value = reading.Text;
            readingPriParam.Value = JoinCodes(reading.Priorities);
            readingCmd.ExecuteNonQuery();
         }

         // Insert senses with POS inheritance
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

            senseEidParam.Value = id;
            senseGlossesParam.Value = string.Join("|", englishGlosses);
            sensePosParam.Value = string.Join("|", posToUse.Select(p => p.Code));
            senseMiscParam.Value = JoinCodes(sense.Miscellanea);
            senseCmd.ExecuteNonQuery();
         }

         id++;
      }

      transaction.Commit();
   }

   static void InsertNameEntries(SqliteConnection connection, List<INameEntry> entries)
   {
      using var transaction = connection.BeginTransaction();

      using var entryCmd = connection.CreateCommand();
      entryCmd.CommandText = "INSERT INTO name_entry (id) VALUES ($id)";
      var entryIdParam = entryCmd.Parameters.Add("$id", SqliteType.Integer);

      using var kanjiCmd = connection.CreateCommand();
      kanjiCmd.CommandText = "INSERT INTO name_kanji (entry_id, text, priorities) VALUES ($eid, $text, $pri)";
      var kanjiEidParam = kanjiCmd.Parameters.Add("$eid", SqliteType.Integer);
      var kanjiTextParam = kanjiCmd.Parameters.Add("$text", SqliteType.Text);
      var kanjiPriParam = kanjiCmd.Parameters.Add("$pri", SqliteType.Text);

      using var readingCmd = connection.CreateCommand();
      readingCmd.CommandText = "INSERT INTO name_reading (entry_id, text, priorities) VALUES ($eid, $text, $pri)";
      var readingEidParam = readingCmd.Parameters.Add("$eid", SqliteType.Integer);
      var readingTextParam = readingCmd.Parameters.Add("$text", SqliteType.Text);
      var readingPriParam = readingCmd.Parameters.Add("$pri", SqliteType.Text);

      using var translationCmd = connection.CreateCommand();
      translationCmd.CommandText = "INSERT INTO name_translation (entry_id, transcriptions) VALUES ($eid, $trans)";
      var transEidParam = translationCmd.Parameters.Add("$eid", SqliteType.Integer);
      var transTransParam = translationCmd.Parameters.Add("$trans", SqliteType.Text);

      long id = 1;
      foreach(var entry in entries)
      {
         entryIdParam.Value = id;
         entryCmd.ExecuteNonQuery();

         foreach(var kanji in entry.Kanjis)
         {
            kanjiEidParam.Value = id;
            kanjiTextParam.Value = kanji.Text;
            kanjiPriParam.Value = JoinCodes(kanji.Priorities);
            kanjiCmd.ExecuteNonQuery();
         }

         foreach(var reading in entry.Readings)
         {
            readingEidParam.Value = id;
            readingTextParam.Value = reading.Text;
            readingPriParam.Value = JoinCodes(reading.Priorities);
            readingCmd.ExecuteNonQuery();
         }

         foreach(var translation in entry.Translations)
         {
            transEidParam.Value = id;
            transTransParam.Value = string.Join("|", translation.Transcriptions);
            translationCmd.ExecuteNonQuery();
         }

         id++;
      }

      transaction.Commit();
   }

   static string JoinCodes<T>(IEnumerable<T> items) where T : notnull
   {
      // Desu's enum types have a Code property (Priority, Miscellaneous, etc.)
      var codes = items.Select(item =>
      {
         var codeProp = item.GetType().GetProperty("Code");
         return codeProp?.GetValue(item)?.ToString() ?? item.ToString() ?? "";
      });
      return string.Join("|", codes);
   }

   static void Execute(SqliteConnection connection, string sql)
   {
      using var cmd = connection.CreateCommand();
      cmd.CommandText = sql;
      cmd.ExecuteNonQuery();
   }
}
