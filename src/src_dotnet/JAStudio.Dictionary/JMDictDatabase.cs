using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.Data.Sqlite;

namespace JAStudio.Dictionary;

public sealed class JMDictDatabase : IDisposable
{
   readonly string _connectionString;

   JMDictDatabase(string connectionString) => _connectionString = connectionString;

   public static JMDictDatabase Open(string dbPath)
   {
      return new JMDictDatabase($"Data Source={dbPath};Mode=ReadOnly");
   }

   public static JMDictDatabase OpenOrGenerate(string dbPath, Action<string>? log = null)
   {
      if(!File.Exists(dbPath))
         JMDictDatabaseGenerator.Generate(dbPath, log);

      return Open(dbPath);
   }

   SqliteConnection OpenConnection()
   {
      var connection = new SqliteConnection(_connectionString);
      connection.Open();
      return connection;
   }

   public List<WordEntry> LookupWord(string text)
   {
      using var connection = OpenConnection();
      var entryIds = LookupEntryIds(connection, "word_kanji", "word_reading", text);
      if(entryIds.Count == 0) return [];

      return LoadWordEntries(connection, entryIds);
   }

   public List<NameEntry> LookupName(string text)
   {
      using var connection = OpenConnection();
      var entryIds = LookupEntryIds(connection, "name_kanji", "name_reading", text);
      if(entryIds.Count == 0) return [];

      return LoadNameEntries(connection, entryIds);
   }

   public bool WordFormExists(string text)
   {
      using var connection = OpenConnection();
      return FormExists(connection, "word_kanji", "word_reading", text);
   }

   public bool NameFormExists(string text)
   {
      using var connection = OpenConnection();
      return FormExists(connection, "name_kanji", "name_reading", text);
   }

   static List<long> LookupEntryIds(SqliteConnection connection, string kanjiTable, string readingTable, string text)
   {
      using var cmd = connection.CreateCommand();
      cmd.CommandText = $"""
         SELECT entry_id FROM {kanjiTable} WHERE text = $text
         UNION
         SELECT entry_id FROM {readingTable} WHERE text = $text
      """;
      cmd.Parameters.AddWithValue("$text", text);

      var ids = new List<long>();
      using var reader = cmd.ExecuteReader();
      while(reader.Read())
         ids.Add(reader.GetInt64(0));

      return ids;
   }

   static bool FormExists(SqliteConnection connection, string kanjiTable, string readingTable, string text)
   {
      using var cmd = connection.CreateCommand();
      cmd.CommandText = $"""
         SELECT 1 FROM {kanjiTable} WHERE text = $text
         UNION ALL
         SELECT 1 FROM {readingTable} WHERE text = $text
         LIMIT 1
      """;
      cmd.Parameters.AddWithValue("$text", text);

      using var reader = cmd.ExecuteReader();
      return reader.Read();
   }

   static List<WordEntry> LoadWordEntries(SqliteConnection connection, List<long> entryIds)
   {
      var inClause = string.Join(",", entryIds);
      var entries = new List<WordEntry>();

      var kanjis = LoadGroups(connection,
         $"SELECT entry_id, text, priorities FROM word_kanji WHERE entry_id IN ({inClause}) ORDER BY entry_id, id",
         r => new WordKanji(r.GetString(1), SplitPipe(r.GetString(2))));

      var readings = LoadGroups(connection,
         $"SELECT entry_id, text, priorities FROM word_reading WHERE entry_id IN ({inClause}) ORDER BY entry_id, id",
         r => new WordReading(r.GetString(1), SplitPipe(r.GetString(2))));

      var senses = LoadGroups(connection,
         $"SELECT entry_id, glosses, pos, misc FROM word_sense WHERE entry_id IN ({inClause}) ORDER BY entry_id, id",
         r => new WordSense(
            SplitPipe(r.GetString(1)),
            SplitPipe(r.GetString(2)),
            SplitPipe(r.GetString(3))));

      foreach(var id in entryIds)
      {
         entries.Add(new WordEntry(
                        id,
                        kanjis.GetValueOrDefault(id, []),
                        readings.GetValueOrDefault(id, []),
                        senses.GetValueOrDefault(id, [])));
      }

      return entries;
   }

   static List<NameEntry> LoadNameEntries(SqliteConnection connection, List<long> entryIds)
   {
      var inClause = string.Join(",", entryIds);
      var entries = new List<NameEntry>();

      var kanjis = LoadGroups(connection,
         $"SELECT entry_id, text, priorities FROM name_kanji WHERE entry_id IN ({inClause}) ORDER BY entry_id, id",
         r => new NameKanji(r.GetString(1), SplitPipe(r.GetString(2))));

      var readings = LoadGroups(connection,
         $"SELECT entry_id, text, priorities FROM name_reading WHERE entry_id IN ({inClause}) ORDER BY entry_id, id",
         r => new NameReading(r.GetString(1), SplitPipe(r.GetString(2))));

      var translations = LoadGroups(connection,
         $"SELECT entry_id, transcriptions FROM name_translation WHERE entry_id IN ({inClause}) ORDER BY entry_id, id",
         r => new NameTranslation(SplitPipe(r.GetString(1))));

      foreach(var id in entryIds)
      {
         entries.Add(new NameEntry(
                        id,
                        kanjis.GetValueOrDefault(id, []),
                        readings.GetValueOrDefault(id, []),
                        translations.GetValueOrDefault(id, [])));
      }

      return entries;
   }

   static Dictionary<long, List<T>> LoadGroups<T>(SqliteConnection connection, string sql, Func<SqliteDataReader, T> mapper)
   {
      var result = new Dictionary<long, List<T>>();

      using var cmd = connection.CreateCommand();
      cmd.CommandText = sql;

      using var reader = cmd.ExecuteReader();
      while(reader.Read())
      {
         var entryId = reader.GetInt64(0);
         if(!result.TryGetValue(entryId, out var list))
         {
            list = [];
            result[entryId] = list;
         }

         list.Add(mapper(reader));
      }

      return result;
   }

   static IReadOnlyList<string> SplitPipe(string value)
      => string.IsNullOrEmpty(value) ? [] : value.Split('|');

   public void Dispose()
   {
      SqliteConnection.ClearPool(new SqliteConnection(_connectionString));
   }
}
