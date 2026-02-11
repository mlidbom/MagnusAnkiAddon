using JAStudio.Core.Note;

namespace JAStudio.Anki;

/// <summary>
/// Implementation of IAnkiCardOperations that uses AnkiFacade to call Python/Anki APIs.
/// Maps domain NoteId to Anki long ID at the boundary.
/// </summary>
public class AnkiCardOperationsImpl : IAnkiCardOperations
{
    readonly AnkiNoteIdMap _idMap;

    public AnkiCardOperationsImpl(AnkiNoteIdMap idMap)
    {
        _idMap = idMap;
    }

    public void SuspendAllCardsForNote(NoteId noteId)
    {
        AnkiFacade.NoteEx.SuspendAllCardsForNote(_idMap.RequireAnkiId(noteId));
    }

    public void UnsuspendAllCardsForNote(NoteId noteId)
    {
        AnkiFacade.NoteEx.UnsuspendAllCardsForNote(_idMap.RequireAnkiId(noteId));
    }
}
