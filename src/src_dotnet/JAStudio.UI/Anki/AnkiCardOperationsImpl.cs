using JAStudio.Core.Anki;

namespace JAStudio.UI.Anki;

/// <summary>
/// Implementation of IAnkiCardOperations that uses AnkiFacade to call Python/Anki APIs.
/// </summary>
internal class AnkiCardOperationsImpl : IAnkiCardOperations
{
    public void SuspendAllCardsForNote(int noteId)
    {
        AnkiFacade.SuspendAllCardsForNote(noteId);
    }

    public void UnsuspendAllCardsForNote(int noteId)
    {
        AnkiFacade.UnsuspendAllCardsForNote(noteId);
    }
}
