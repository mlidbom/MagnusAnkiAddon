using System.Collections.Generic;
using System.Linq;
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
      using var db = AnkiDb.OpenReadOnly(dbFilePath);

      // Fetch all note types in C# to avoid depending on Anki's custom unicase collation
      var allNoteTypes = db.NoteTypes.ToList();
      var noteTypeIds = allNoteTypes
                       .Where(nt => NoteTypes.All.Contains(nt.Name))
                       .ToDictionary(nt => nt.Id, nt => nt.Name);

      if(noteTypeIds.Count == 0)
         return [];

      var noteTypeIdList = noteTypeIds.Keys.ToList();

      var results = (from card in db.Cards
                     join note in db.Notes on card.NoteId equals note.Id
                     join template in db.Templates on new { note.NoteTypeId, card.Ordinal } equals new { template.NoteTypeId, template.Ordinal }
                     where noteTypeIdList.Contains(note.NoteTypeId)
                     select new { card.NoteId, template.Name, card.Queue, note.NoteTypeId })
        .ToList();

      return results.Select(r => new CardStudyingStatus(r.NoteId, r.Name, r.Queue == QueueTypeSuspended, noteTypeIds[r.NoteTypeId])).ToList();
   }
}
