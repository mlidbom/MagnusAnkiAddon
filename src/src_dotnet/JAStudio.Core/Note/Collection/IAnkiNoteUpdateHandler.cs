using JAStudio.Core.Note;

namespace JAStudio.Core.Note.Collection;

public interface IAnkiNoteUpdateHandler
{
   void AnkiNoteAdded(long ankiNoteId, NoteData data);
   void AnkiNoteWillFlush(long ankiNoteId, NoteData data);
   void AnkiNoteRemoved(long ankiNoteId);
   void OnNoteUpdated(dynamic listener);

   /// <summary>
   /// Returns the Anki long note ID for the given domain NoteId.
   /// Used by the Python sync layer to find the Anki note when syncing changes back.
   /// </summary>
   long GetAnkiNoteId(NoteId noteId);
}
