using System;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Sentences;

public class SentenceUserFields
{
    private readonly SentenceNote _sentence;
    private readonly Func<string, string> _getField;
    private readonly Action<string, string> _setField;

    public SentenceUserFields(SentenceNote sentence, Func<string, string> getField, Action<string, string> setField)
    {
        _sentence = sentence;
        _getField = getField;
        _setField = setField;
    }

    public MutableStringField Comments => new(SentenceNoteFields.UserComments, _getField, _setField);
    public MutableStringField Answer => new(SentenceNoteFields.UserAnswer, _getField, _setField);
    public MutableStringField Question => new(SentenceNoteFields.UserQuestion, _getField, _setField);
}
