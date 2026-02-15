namespace JAStudio.Core.Note.NoteFields;

public class IntegerField
{
    private readonly MutableStringField _field;

    public IntegerField(MutableStringField field)
    {
        _field = field;
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
