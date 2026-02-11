namespace JAStudio.Core.Note.Collection;

public class CardStudyingStatus
{
    public long ExternalNoteId { get; }
    public string CardType { get; }
    public bool IsSuspended { get; }
    public string NoteTypeName { get; }

    public CardStudyingStatus(long externalNoteId, string cardType, bool isSuspended, string noteTypeName)
    {
        ExternalNoteId = externalNoteId;
        CardType = cardType;
        IsSuspended = isSuspended;
        NoteTypeName = noteTypeName;
    }
}
