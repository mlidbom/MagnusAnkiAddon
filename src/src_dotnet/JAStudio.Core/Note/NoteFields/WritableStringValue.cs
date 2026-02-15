using System;
using Compze.Utilities.SystemCE.ReactiveCE;

namespace JAStudio.Core.Note.NoteFields;

public class WritableStringValue : IWritableStringValue, IObservable<string>
{
   readonly NoteGuard _guard;
   readonly SimpleObservable<string> _observable = new();
   string _value;

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
            _observable.OnNext(trimmed);
         });
      }
   }

   public void Empty() => Set(string.Empty);

   public bool HasValue() => !string.IsNullOrEmpty(_value);

   public IDisposable Subscribe(IObserver<string> observer) => _observable.Subscribe(observer);

   public override string ToString() => _value;
}
