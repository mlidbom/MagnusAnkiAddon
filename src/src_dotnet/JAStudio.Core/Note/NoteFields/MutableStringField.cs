namespace JAStudio.Core.Note.NoteFields;

public class MutableStringField
{
    private readonly JPNote _note;
    private readonly string _fieldName;

    public MutableStringField(JPNote note, string fieldName)
    {
        _note = note;
        _fieldName = fieldName;
    }

    public string Value => _note.GetField(_fieldName);

    public void Set(string value)
    {
        _note.SetField(_fieldName, value);
    }

    public void Empty()
    {
        Set(string.Empty);
    }

    public bool HasValue()
    {
        return !string.IsNullOrEmpty(Value);
    }

    public override string ToString()
    {
        return Value;
    }
}
