namespace JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

public class FieldWrapper<TValue, TWrapper>
{
    private readonly SerializedObjectField<TWrapper> _field;
    private readonly ValueWrapper<TValue> _value;

    public FieldWrapper(SerializedObjectField<TWrapper> field, ValueWrapper<TValue> value)
    {
        _field = field;
        _value = value;
    }

    public void Set(TValue value)
    {
        _value.Set(value);
        _field.Save();
    }

    public TValue Get()
    {
        return _value.Get();
    }

    public override string ToString()
    {
        return _value.ToString();
    }
}
