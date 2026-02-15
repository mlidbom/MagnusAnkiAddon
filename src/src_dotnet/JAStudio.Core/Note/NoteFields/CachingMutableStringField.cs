using Compze.Utilities.SystemCE;
using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.NoteFields;

public class CachingMutableStringField
{
    readonly string _fieldName;
    readonly Func<string, string> _getter;
    readonly Action<string, string> _setter;
    List<Action>? _resetCallbacks;
    string _value;

    public CachingMutableStringField(string fieldName, Func<string, string> getter, Action<string, string> setter)
    {
        _fieldName = fieldName;
        _getter = getter;
        _setter = setter;
        _resetCallbacks = null;
        _value = _getter(_fieldName);
    }

    public string Value => _value;

    public void Set(string value)
    {
        var newValue = value.Trim();
        if (newValue != _value)
        {
            _setter(_fieldName, value.Trim());
            _value = newValue;
            
            if (_resetCallbacks != null)
            {
                foreach (var callback in _resetCallbacks)
                {
                    callback();
                }
            }
        }
    }

    public bool HasValue()
    {
        return !string.IsNullOrEmpty(Value);
    }

    public void Empty()
    {
        Set(string.Empty);
    }

    public LazyCE<TValue> LazyReader<TValue>(Func<TValue> reader) where TValue : class
    {
        var lazy = new LazyCE<TValue>(reader);
        OnChange(lazy.Reset);
        return lazy;
    }

    public void OnChange(Action callback)
    {
        _resetCallbacks ??= new List<Action>();
        _resetCallbacks.Add(callback);
    }

    public override string ToString()
    {
        return Value;
    }
}
