// ReSharper disable UnusedMember.Global used from python
namespace JAStudio.Core.Note.Collection;

public interface IExternalNoteUpdateHandler
{
   void ExternalNoteAdded(long externalNoteId, NoteData data);
   void ExternalNoteWillFlush(long externalNoteId, NoteData data);
   void ExternalNoteRemoved(long externalNoteId);
   void OnNoteUpdated(dynamic listener);
   long GetExternalNoteId(NoteId noteId);
}
