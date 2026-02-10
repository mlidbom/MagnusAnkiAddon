namespace JAStudio.Core.Note.Collection;

public class CardStudyingStatus
{
    public long AnkiNoteId { get; }
    public string CardType { get; }
    public bool IsSuspended { get; }
    public string NoteTypeName { get; }

    public CardStudyingStatus(long ankiNoteId, string cardType, bool isSuspended, string noteTypeName)
    {
        AnkiNoteId = ankiNoteId;
        CardType = cardType;
        IsSuspended = isSuspended;
        NoteTypeName = noteTypeName;
    }
}
