using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.NoteFields;

public class MutableStringField : IWritableStringValue
{
    readonly string _fieldName;
    readonly Func<string, string> _getter;
    readonly Action<string, string> _setter;

    public MutableStringField(string fieldName, Func<string, string> getter, Action<string, string> setter)
    {
        _fieldName = fieldName;
        _getter = getter;
        _setter = setter;
    }

    public string Value => _getter(_fieldName);

    public void Set(string value)
    {
        _setter(_fieldName, value);
    }

    public void Empty()
    {
        Set(string.Empty);
    }

    public bool HasValue()
    {
        return !string.IsNullOrEmpty(Value);
    }

    public List<MediaReference> GetImageReferences() => MediaFieldParsing.ParseImageReferences(Value);

    public override string ToString()
    {
        return Value;
    }
}
