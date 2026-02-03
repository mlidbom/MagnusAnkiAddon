using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.NoteFields;

public class MutableCommaSeparatedStringsListField
{
    private readonly MutableStringField _field;

    public MutableCommaSeparatedStringsListField(JPNote note, string fieldName)
    {
        _field = new MutableStringField(note, fieldName);
    }

    public List<string> Get()
    {
        var value = _field.Value;
        if (string.IsNullOrWhiteSpace(value))
        {
            return new List<string>();
        }

        return value.Split(',')
            .Select(s => s.Trim())
            .Where(s => !string.IsNullOrEmpty(s))
            .ToList();
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

    public override string ToString()
    {
        return string.Join(", ", Get());
    }
}
