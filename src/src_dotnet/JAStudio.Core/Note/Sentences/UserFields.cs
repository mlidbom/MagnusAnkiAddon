using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Sentences;

public class SentenceUserFields
{
    private readonly SentenceNote _sentence;

    public SentenceUserFields(SentenceNote sentence)
    {
        _sentence = sentence;
    }

    public MutableStringField Comments => new(_sentence, SentenceNoteFields.UserComments);
    public MutableStringField Answer => new(_sentence, SentenceNoteFields.UserAnswer);
    public MutableStringField Question => new(_sentence, SentenceNoteFields.UserQuestion);
}
