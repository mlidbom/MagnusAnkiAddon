using JAStudio.Core.Note;

namespace JAStudio.Core.Note.Collection;

public interface IExternalNoteUpdateHandler
{
   void ExternalNoteAdded(long externalNoteId, NoteData data);
   void ExternalNoteWillFlush(long externalNoteId, NoteData data);
   void ExternalNoteRemoved(long externalNoteId);
   void OnNoteUpdated(dynamic listener);

   /// <summary>
   /// Returns the external long note ID for the given domain NoteId.
   /// Used by the Python sync layer to find the external note when syncing changes back.
   /// </summary>
   long GetExternalNoteId(NoteId noteId);
}
