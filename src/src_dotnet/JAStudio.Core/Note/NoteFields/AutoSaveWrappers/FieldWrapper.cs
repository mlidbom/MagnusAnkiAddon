using System;

namespace JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

public class FieldWrapper<TValue, TWrapper>
{
    private readonly Action _save;
    private readonly ValueWrapper<TValue> _value;

    public FieldWrapper(Action save, ValueWrapper<TValue> value)
    {
        _save = save;
        _value = value;
    }

    public void Set(TValue value)
    {
        _value.Set(value);
        _save();
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
