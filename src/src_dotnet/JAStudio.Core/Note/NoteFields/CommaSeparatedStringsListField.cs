using Compze.Utilities.SystemCE;
using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.NoteFields;

public class MutableCommaSeparatedStringsListField
{
    private readonly CachingMutableStringField _field;
    private readonly LazyCE<List<string>> _value;

    public MutableCommaSeparatedStringsListField(CachingMutableStringField field)
    {
        _field = field;
        _value = _field.LazyReader(ParseValue);
    }

    private List<string> ParseValue()
    {
        return StringExtensions.ExtractCommaSeparatedValues(_field.Value);
    }

    public List<string> Get()
    {
        return _value.Value;
    }

    public void Remove(string remove)
    {
        Set(Get().Where(item => item != remove).ToList());
    }

    public virtual void Set(List<string> value)
    {
        _field.Set(string.Join(", ", value));
    }

    public string RawStringValue()
    {
        return _field.Value;
    }

    public void Add(string add)
    {
        var current = Get();
        current.Add(add);
        Set(current);
    }

    public LazyCE<TValue> LazyReader<TValue>(Func<TValue> reader) where TValue : class
    {
        return _field.LazyReader(reader);
    }

    public override string ToString()
    {
        return string.Join(", ", Get());
    }
}
