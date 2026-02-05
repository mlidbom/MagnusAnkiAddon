using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

public class FieldSetWrapper<TValue>
{
    private const string Secret = "aoeulrcaboeusthb";
    private readonly Action _save;
    private readonly Func<HashSet<TValue>> _value;

    private FieldSetWrapper(Action saveCallback, Func<HashSet<TValue>> value, string secret)
    {
        if (Secret != secret)
            throw new ArgumentException("use the factory methods, not this private constructor");
        _save = saveCallback;
        _value = value; // never replace _value or the save method will stop working...
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

    public static FieldSetWrapper<TValue> ForJsonObjectField<TWrapper>(MutableSerializedObjectField<TWrapper> field, HashSet<TValue> value)
    {
        return new FieldSetWrapper<TValue>(() => field.Save(), () => value, Secret);
    }

    public override string ToString()
    {
        var set = _value();
        return set != null ? string.Join(", ", set) : "{}";
    }
}
