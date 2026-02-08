namespace JAStudio.Core.Note.Collection;

public interface IAnkiNoteUpdateHandler
{
   void AnkiNoteAdded(NoteData data);
   void AnkiNoteWillFlush(NoteData data);
   void AnkiNoteRemoved(long noteId);
   void OnNoteUpdated(dynamic listener);
}
