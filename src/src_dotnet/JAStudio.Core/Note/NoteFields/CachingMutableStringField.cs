using Compze.Utilities.SystemCE;
using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.NoteFields;

public class CachingMutableStringField
{
    private readonly JPNote _note;
    private readonly string _fieldName;
    private List<Action>? _resetCallbacks;
    private string _value;

    public CachingMutableStringField(JPNote note, string fieldName)
    {
        _note = note;
        _fieldName = fieldName;
        _resetCallbacks = null;
        _value = GetInitialValueForCaching();
    }

    private string GetInitialValueForCaching()
    {
        return _note.GetField(_fieldName);
    }

    public string Value => _value;

    public void Set(string value)
    {
        var newValue = value.Trim();
        if (newValue != _value)
        {
            _note.SetField(_fieldName, value.Trim());
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
