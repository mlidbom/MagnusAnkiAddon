using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.NoteFields;

public class WritableStringValue : IWritableStringValue
{
   readonly Func<string> _getValue;
   readonly Action<string> _setValue;
   List<Action>? _changeCallbacks;

   public WritableStringValue(Func<string> getValue, Action<string> setValue)
   {
      _getValue = getValue;
      _setValue = setValue;
   }

   public string Value => _getValue();

   public void Set(string value)
   {
      var trimmed = value.Trim();
      if (trimmed != Value)
      {
         _setValue(trimmed);
      }
   }

   public void Empty() => Set(string.Empty);

   public bool HasValue() => !string.IsNullOrEmpty(Value);

   public void OnChange(Action callback)
   {
      _changeCallbacks ??= [];
      _changeCallbacks.Add(callback);
   }

   internal void NotifyChanged()
   {
      if (_changeCallbacks == null) return;
      foreach (var callback in _changeCallbacks)
      {
         callback();
      }
   }

   public override string ToString() => Value;
}
