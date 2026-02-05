namespace JAStudio.Core.Note.NoteFields;

public class IntegerField
{
    private readonly JPNote _note;
    private readonly MutableStringField _field;

    public IntegerField(JPNote note, string fieldName)
    {
        _note = note;
        _field = new MutableStringField(note, fieldName);
    }

    public int Get()
    {
        return _field.HasValue() && int.TryParse(_field.Value, out var value) ? value : 0;
    }

    public void Set(int value)
    {
        _field.Set(value.ToString());
    }
}
