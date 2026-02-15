using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Anki;

/// <summary>
/// Fetches card studying statuses directly from Anki's SQLite database.
/// Port of jastudio.note.studing_status_helper.fetch_card_studying_statuses.
/// </summary>
public static class CardStudyingStatusLoader
{
   /// <summary>Anki queue type value for suspended cards.</summary>
   const int QueueTypeSuspended = -1;

   /// <summary>
   /// Fetch studying status for all cards belonging to known note types (Kanji, Vocab, Sentence).
   /// Opens and closes its own connection so it's safe to call from any thread.
   /// </summary>
   public static List<CardStudyingStatus> FetchAll(string dbFilePath)
   {
      using var db = AnkiDatabase.OpenReadOnly(dbFilePath);

      // First get the note type IDs for our known types by scanning in C# (avoids unicase collation issues)
      var noteTypeIds = new Dictionary<long, string>();
      using (var ntCmd = db.Connection.CreateCommand())
      {
         ntCmd.CommandText = "SELECT id, name FROM notetypes";
         using var ntReader = ntCmd.ExecuteReader();
         while (ntReader.Read())
         {
            var name = ntReader.GetString(1);
            if (NoteTypes.All.Contains(name))
               noteTypeIds[ntReader.GetInt64(0)] = name;
         }
      }

      if (noteTypeIds.Count == 0)
         return [];

      // Build the IN clause with the numeric IDs (no collation needed)
      var idList = string.Join(",", noteTypeIds.Keys);
      using var cmd = db.Connection.CreateCommand();
      cmd.CommandText = $"""
                         SELECT cards.nid   AS note_id,
                                templates.name AS card_type,
                                cards.queue AS queue,
                                notes.mid AS note_type_id
                         FROM cards
                         JOIN notes ON cards.nid = notes.id
                         JOIN templates ON templates.ntid = notes.mid AND templates.ord = cards.ord
                         WHERE notes.mid IN ({idList})
                         """;

      using var reader = cmd.ExecuteReader();
      var results = new List<CardStudyingStatus>();

      while (reader.Read())
      {
         var noteId = reader.GetInt64(0);
         var cardType = reader.GetString(1);
         var isSuspended = reader.GetInt32(2) == QueueTypeSuspended;
         var noteTypeId = reader.GetInt64(3);
         var noteTypeName = noteTypeIds[noteTypeId];

         results.Add(new CardStudyingStatus(noteId, cardType, isSuspended, noteTypeName));
      }

      return results;
   }
}
