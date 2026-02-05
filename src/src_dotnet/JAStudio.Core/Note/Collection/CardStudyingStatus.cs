namespace JAStudio.Core.Note.Collection;

public class CardStudyingStatus
{
    public int NoteId { get; }
    public string CardType { get; }
    public bool IsSuspended { get; }
    public string NoteTypeName { get; }

    public CardStudyingStatus(int noteId, string cardType, bool isSuspended, string noteTypeName)
    {
        NoteId = noteId;
        CardType = cardType;
        IsSuspended = isSuspended;
        NoteTypeName = noteTypeName;
    }
}
