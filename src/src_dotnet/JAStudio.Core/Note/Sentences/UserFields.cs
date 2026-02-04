using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Sentences;

public class SentenceUserFields
{
    private readonly SentenceNote _sentence;

    public SentenceUserFields(SentenceNote sentence)
    {
        _sentence = sentence;
    }

    public MutableStringField Comments => new(_sentence, NoteFieldsConstants.Sentence.UserComments);
    public MutableStringField Answer => new(_sentence, NoteFieldsConstants.Sentence.UserAnswer);
    public MutableStringField Question => new(_sentence, NoteFieldsConstants.Sentence.UserQuestion);
}
