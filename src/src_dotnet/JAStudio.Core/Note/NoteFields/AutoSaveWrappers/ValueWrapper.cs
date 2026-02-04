namespace JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

public class ValueWrapper<TValue>
{
    private TValue _value;

    public ValueWrapper(TValue value)
    {
        _value = value;
    }

    public void Set(TValue value)
    {
        _value = value;
    }

    public TValue Get()
    {
        return _value;
    }

    public override string ToString()
    {
        return _value?.ToString() ?? string.Empty;
    }
}
