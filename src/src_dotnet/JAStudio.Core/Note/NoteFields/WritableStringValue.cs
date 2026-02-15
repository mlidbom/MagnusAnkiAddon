using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.NoteFields;

public class WritableStringValue : IWritableStringValue
{
   readonly NoteGuard _guard;
   string _value;
   List<Action>? _changeCallbacks;

   public WritableStringValue(string initialValue, NoteGuard guard)
   {
      _value = initialValue;
      _guard = guard;
   }

   public string Value => _value;

   public void Set(string value)
   {
      var trimmed = value.Trim();
      if(trimmed != _value)
      {
         _guard.Update(() =>
         {
            _value = trimmed;
            NotifyChanged();
         });
      }
   }

   public void Empty() => Set(string.Empty);

   public bool HasValue() => !string.IsNullOrEmpty(_value);

   public void OnChange(Action callback)
   {
      _changeCallbacks ??= [];
      _changeCallbacks.Add(callback);
   }

   void NotifyChanged()
   {
      if(_changeCallbacks == null) return;
      foreach(var callback in _changeCallbacks)
      {
         callback();
      }
   }

   public override string ToString() => _value;
}
