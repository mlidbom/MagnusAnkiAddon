using System;

namespace JAStudio.Core.Anki;

/// <summary>
/// Interface for Anki card operations that must be implemented by the UI layer.
/// This allows JAStudio.Core to request card operations without depending on JAStudio.UI.
/// </summary>
public interface IAnkiCardOperations
{
    /// <summary>Suspend all cards for the given note ID.</summary>
    void SuspendAllCardsForNote(long noteId);

    /// <summary>Unsuspend all cards for the given note ID.</summary>
    void UnsuspendAllCardsForNote(long noteId);
}

/// <summary>
/// Service locator for Anki card operations.
/// JAStudio.UI must call SetImplementation() during initialization.
/// </summary>
public class AnkiCardOperations
{
    internal AnkiCardOperations() {}

    static IAnkiCardOperations? _implementation;

    /// <summary>
    /// Set the implementation of card operations (called by JAStudio.UI during initialization).
    /// </summary>
    public void SetImplementation(IAnkiCardOperations implementation)
    {
        _implementation = implementation;
    }

    /// <summary>Suspend all cards for the given note ID.</summary>
    public void SuspendAllCardsForNote(long noteId)
    {
        if (_implementation == null)
        {
            throw new InvalidOperationException(
                "AnkiCardOperations.SetImplementation() must be called before using card operations");
        }

        _implementation.SuspendAllCardsForNote(noteId);
    }

    /// <summary>Unsuspend all cards for the given note ID.</summary>
    public void UnsuspendAllCardsForNote(long noteId)
    {
        if (_implementation == null)
        {
            throw new InvalidOperationException(
                "AnkiCardOperations.SetImplementation() must be called before using card operations");
        }

        _implementation.UnsuspendAllCardsForNote(noteId);
    }
}
