using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

public class FieldSetWrapper<TValue>
{
    private readonly Action _save;
    private readonly Func<HashSet<TValue>> _value;

    public FieldSetWrapper(Action saveCallback, Func<HashSet<TValue>> value)
    {
        _save = saveCallback;
        _value = value;
    }

    public HashSet<TValue> Get() => _value();

    public void Add(TValue value)
    {
        _value().Add(value);
        _save();
    }

    public void Remove(TValue key)
    {
        _value().Remove(key);
        _save();
    }

    public void Discard(TValue key)
    {
        _value().Remove(key);
        _save();
    }

    public void Clear() => _value().Clear();

    public void OverwriteWith(FieldSetWrapper<TValue> other)
    {
        _value().Clear();
        foreach (var item in other.Get())
        {
            _value().Add(item);
        }
        _save();
    }

    public bool None() => !Any();
    public bool Any() => _value().Any();

    public override string ToString()
    {
        var set = _value();
        return set != null ? string.Join(", ", set) : "{}";
    }
}
