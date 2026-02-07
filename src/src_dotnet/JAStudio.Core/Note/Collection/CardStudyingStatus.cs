namespace JAStudio.Core.Note.Collection;

public class CardStudyingStatus
{
    public long NoteId { get; }
    public string CardType { get; }
    public bool IsSuspended { get; }
    public string NoteTypeName { get; }

    public CardStudyingStatus(long noteId, string cardType, bool isSuspended, string noteTypeName)
    {
        NoteId = noteId;
        CardType = cardType;
        IsSuspended = isSuspended;
        NoteTypeName = noteTypeName;
    }
}
