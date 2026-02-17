using System;
using System.Collections.Generic;
using JAStudio.Core.Anki;
using JAStudio.Core.Note;
using Microsoft.Data.Sqlite;

namespace JAStudio.Anki;

/// <summary>
/// Result from bulk loading notes from Anki's SQLite database.
/// Contains both the domain NoteData (with Guid-based IDs) and the Anki ID mapping.
/// </summary>
public class AnkiBulkLoadResult
{
   public List<NoteData> Notes { get; }
   public Dictionary<long, NoteId> AnkiIdMap { get; }

   public AnkiBulkLoadResult(List<NoteData> notes, Dictionary<long, NoteId> ankiIdMap)
   {
      Notes = notes;
      AnkiIdMap = ankiIdMap;
   }
}

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
   public static AnkiBulkLoadResult LoadAllNotesOfType(string dbFilePath, string noteTypeName, Func<Guid, NoteId> idFactory)
   {
      using var db = AnkiDatabase.OpenReadOnly(dbFilePath);
      var (noteTypeId, fieldMap, fieldCount) = GetNoteTypeInfo(db.Connection, noteTypeName);
      return LoadNotes(db.Connection, noteTypeId, fieldMap, fieldCount, idFactory);
   }

   /// <summary>
   /// Build a lightweight AnkiNoteId → domain NoteId mapping for all known note types.
   /// Only reads the jas_note_id field — does not load full note data.
   /// </summary>
   public static Dictionary<long, NoteId> LoadAnkiIdMaps(string dbFilePath)
   {
      using var db = AnkiDatabase.OpenReadOnly(dbFilePath);
      var result = new Dictionary<long, NoteId>();

      foreach(var noteTypeName in NoteTypes.AllList)
      {
         var idFactory = NoteTypes.IdFactoryFromName(noteTypeName);
         var (noteTypeId, fieldMap, _) = GetNoteTypeInfo(db.Connection, noteTypeName);

         if(!fieldMap.TryGetValue(AnkiFieldNames.JasNoteId, out var jasNoteIdOrdinal))
            continue;

         using var cmd = db.Connection.CreateCommand();
         cmd.CommandText = """
                           SELECT notes.id, notes.flds
                           FROM notes
                           WHERE notes.mid = @mid
                           """;
         cmd.Parameters.AddWithValue("@mid", noteTypeId);

         using var reader = cmd.ExecuteReader();
         while(reader.Read())
         {
            var ankiId = reader.GetInt64(0);
            var fldsRaw = reader.IsDBNull(1) ? "" : reader.GetString(1);
            var fieldValues = string.IsNullOrEmpty(fldsRaw) ? [] : fldsRaw.Split(FieldSeparator);

            var jasNoteIdStr = jasNoteIdOrdinal < fieldValues.Length ? fieldValues[jasNoteIdOrdinal] : "";
            if(Guid.TryParse(jasNoteIdStr, out var guid))
            {
               result[ankiId] = idFactory(guid);
            }
         }
      }

      return result;
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
      while(ntReader.Read())
      {
         if(string.Equals(ntReader.GetString(1), noteTypeName, StringComparison.Ordinal))
         {
            noteTypeId = ntReader.GetInt64(0);
            break;
         }
      }

      if(noteTypeId == null)
         throw new KeyNotFoundException($"Note type '{noteTypeName}' not found in Anki database.");

      // Get field name → ordinal mapping
      using var fCmd = connection.CreateCommand();
      fCmd.CommandText = "SELECT name, ord FROM fields WHERE ntid = @ntid ORDER BY ord";
      fCmd.Parameters.AddWithValue("@ntid", noteTypeId);

      var fieldMap = new Dictionary<string, int>();
      using var reader = fCmd.ExecuteReader();
      while(reader.Read())
      {
         var name = reader.GetString(0);
         var ord = reader.GetInt32(1);
         fieldMap[name] = ord;
      }

      return (noteTypeId.Value, fieldMap, fieldMap.Count);
   }

   static AnkiBulkLoadResult LoadNotes(SqliteConnection connection, long noteTypeId, Dictionary<string, int> fieldMap, int fieldCount, Func<Guid, NoteId> idFactory)
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
      var ankiIdMap = new Dictionary<long, NoteId>();

      while(reader.Read())
      {
         var ankiId = reader.GetInt64(0);

         var tagsRaw = reader.IsDBNull(1) ? "" : reader.GetString(1);
         var tags = string.IsNullOrEmpty(tagsRaw)
                       ? new List<string>()
                       : new List<string>(tagsRaw.Split(' ', StringSplitOptions.RemoveEmptyEntries));

         var fldsRaw = reader.IsDBNull(2) ? "" : reader.GetString(2);
         var fieldValues = string.IsNullOrEmpty(fldsRaw)
                              ? []
                              : fldsRaw.Split(FieldSeparator);

         var fields = new Dictionary<string, string>(fieldMap.Count);
         foreach(var (name, ordinal) in fieldMap)
         {
            fields[name] = ordinal < fieldValues.Length ? fieldValues[ordinal] : "";
         }

         // Read persisted jas_note_id from the note's fields, or generate a new one.
         // A new GUID is written back to the jas_note_id field on next flush.
         var jasNoteIdStr = fields.GetValueOrDefault(AnkiFieldNames.JasNoteId, "");
         var noteId = Guid.TryParse(jasNoteIdStr, out var guid)
                         ? idFactory(guid)
                         : idFactory(Guid.NewGuid());

         ankiIdMap[ankiId] = noteId;
         results.Add(new NoteData(noteId, fields, tags));
      }

      return new AnkiBulkLoadResult(results, ankiIdMap);
   }
}
