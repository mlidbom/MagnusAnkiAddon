namespace JAStudio.Core.Anki;

/// <summary>
/// Implementation of IAnkiCardOperations that uses AnkiFacade to call Python/Anki APIs.
/// </summary>
public class AnkiCardOperationsImpl : IAnkiCardOperations
{
    public void SuspendAllCardsForNote(int noteId)
    {
        AnkiFacade.NoteEx.SuspendAllCardsForNote(noteId);
    }

    public void UnsuspendAllCardsForNote(int noteId)
    {
        AnkiFacade.NoteEx.UnsuspendAllCardsForNote(noteId);
    }
}
