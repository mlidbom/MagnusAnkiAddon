using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using Microsoft.Data.Sqlite;

namespace JAStudio.Core.Anki;

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
   /// </summary>
   public static List<CardStudyingStatus> FetchAll(AnkiDatabase db)
   {
      using var cmd = db.Connection.CreateCommand();
      cmd.CommandText = $"""
                         SELECT cards.nid   AS note_id,
                                templates.name AS card_type,
                                cards.queue AS queue,
                                notetypes.name AS note_type
                         FROM cards
                         JOIN notes ON cards.nid = notes.id
                         JOIN notetypes ON notetypes.id = notes.mid
                         JOIN templates ON templates.ntid = notes.mid AND templates.ord = cards.ord
                         WHERE notetypes.name COLLATE NOCASE IN (@sentence, @vocab, @kanji)
                         """;

      cmd.Parameters.AddWithValue("@sentence", NoteTypes.Sentence);
      cmd.Parameters.AddWithValue("@vocab", NoteTypes.Vocab);
      cmd.Parameters.AddWithValue("@kanji", NoteTypes.Kanji);

      using var reader = cmd.ExecuteReader();
      var results = new List<CardStudyingStatus>();

      while (reader.Read())
      {
         var noteId = reader.GetInt64(0);
         var cardType = reader.GetString(1);
         var isSuspended = reader.GetInt32(2) == QueueTypeSuspended;
         var noteTypeName = reader.GetString(3);

         results.Add(new CardStudyingStatus(noteId, cardType, isSuspended, noteTypeName));
      }

      return results;
   }
}
