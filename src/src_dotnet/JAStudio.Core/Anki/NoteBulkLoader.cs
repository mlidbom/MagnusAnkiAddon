using System;
using System.Collections.Generic;
using JAStudio.Core.Note;
using Microsoft.Data.Sqlite;

namespace JAStudio.Core.Anki;

/// <summary>
/// Loads all notes of a given note type directly from Anki's SQLite database.
/// Port of jastudio.anki_extentions.note_bulk_loader.NoteBulkLoader.
/// </summary>
public static class NoteBulkLoader
{
   const char FieldSeparator = '\x1f';

   /// <summary>
   /// Load all notes of the specified note type from the Anki database.
   /// Opens and closes its own connection so it's safe to call from any thread.
   /// </summary>
   public static List<NoteData> LoadAllNotesOfType(string dbFilePath, string noteTypeName)
   {
      using var db = AnkiDatabase.OpenReadOnly(dbFilePath);
      var (noteTypeId, fieldMap, fieldCount) = GetNoteTypeInfo(db.Connection, noteTypeName);
      return LoadNotes(db.Connection, noteTypeId, fieldMap, fieldCount);
   }

   static (long noteTypeId, Dictionary<string, int> fieldMap, int fieldCount) GetNoteTypeInfo(SqliteConnection connection, string noteTypeName)
   {
      // Get note type ID.
      // The notetypes.name column has COLLATE unicase (Anki custom). To avoid depending on that
      // collation working correctly, we fetch all note types and match in C#.
      using var ntCmd = connection.CreateCommand();
      ntCmd.CommandText = "SELECT id, name FROM notetypes";
      using var ntReader = ntCmd.ExecuteReader();

      long? noteTypeId = null;
      while (ntReader.Read())
      {
         if (string.Equals(ntReader.GetString(1), noteTypeName, StringComparison.Ordinal))
         {
            noteTypeId = ntReader.GetInt64(0);
            break;
         }
      }

      if (noteTypeId == null)
         throw new KeyNotFoundException($"Note type '{noteTypeName}' not found in Anki database.");

      // Get field name → ordinal mapping
      using var fCmd = connection.CreateCommand();
      fCmd.CommandText = "SELECT name, ord FROM fields WHERE ntid = @ntid ORDER BY ord";
      fCmd.Parameters.AddWithValue("@ntid", noteTypeId);

      var fieldMap = new Dictionary<string, int>();
      using var reader = fCmd.ExecuteReader();
      while (reader.Read())
      {
         var name = reader.GetString(0);
         var ord = reader.GetInt32(1);
         fieldMap[name] = ord;
      }

      return (noteTypeId.Value, fieldMap, fieldMap.Count);
   }

   static List<NoteData> LoadNotes(SqliteConnection connection, long noteTypeId, Dictionary<string, int> fieldMap, int fieldCount)
   {
      using var cmd = connection.CreateCommand();
      cmd.CommandText = """
                        SELECT notes.id,
                               notes.tags,
                               notes.flds
                        FROM notes
                        WHERE notes.mid = @mid
                        """;
      cmd.Parameters.AddWithValue("@mid", noteTypeId);

      using var reader = cmd.ExecuteReader();
      var results = new List<NoteData>();

      while (reader.Read())
      {
         var id = reader.GetInt64(0);

         var tagsRaw = reader.IsDBNull(1) ? "" : reader.GetString(1);
         var tags = string.IsNullOrEmpty(tagsRaw)
            ? new List<string>()
            : new List<string>(tagsRaw.Split(' ', System.StringSplitOptions.RemoveEmptyEntries));

         var fldsRaw = reader.IsDBNull(2) ? "" : reader.GetString(2);
         var fieldValues = string.IsNullOrEmpty(fldsRaw)
            ? System.Array.Empty<string>()
            : fldsRaw.Split(FieldSeparator);

         var fields = new Dictionary<string, string>(fieldMap.Count);
         foreach (var (name, ordinal) in fieldMap)
         {
            fields[name] = ordinal < fieldValues.Length ? fieldValues[ordinal] : "";
         }

         results.Add(new NoteData(id, fields, tags));
      }

      return results;
   }
}
