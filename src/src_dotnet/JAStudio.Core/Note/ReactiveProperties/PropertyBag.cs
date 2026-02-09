using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// A simple observable that fires a notification on demand. Used as a change signal.
/// </summary>
public class Signal : IObservable<object?>, IDisposable
{
   List<IObserver<object?>>? _observers;

   public void Fire()
   {
      if (_observers == null) return;
      for (var i = 0; i < _observers.Count; i++)
      {
         _observers[i].OnNext(null);
      }
   }

   public IDisposable Subscribe(IObserver<object?> observer)
   {
      _observers ??= [];
      var sub = new SignalSubscription(this, observer);
      _observers.Add(observer);
      return sub;
   }

   public void Dispose()
   {
      if (_observers != null)
      {
         foreach (var obs in _observers) obs.OnCompleted();
         _observers.Clear();
         _observers = null;
      }
   }

   void Remove(IObserver<object?> observer) => _observers?.Remove(observer);

   sealed class SignalSubscription(Signal signal, IObserver<object?> observer) : IDisposable
   {
      public void Dispose() => signal.Remove(observer);
   }
}

/// <summary>
/// Manages all properties for a note. Handles:
/// - Registration of properties with their Anki field name and serialization
/// - Bulk loading from a Dictionary (Anki boundary inbound)
/// - Bulk serialization to a Dictionary (Anki boundary outbound)
/// - Aggregated change notification (any property change fires AnyChanged)
/// </summary>
public class PropertyBag : IDisposable
{
   readonly List<IRegisteredProperty> _properties = [];
   readonly List<IDisposable> _subscriptions = [];
   readonly Signal _anyChanged = new();
   bool _isSilent;

   /// <summary>
   /// Fires whenever any registered property changes.
   /// Subscribe to this for flush triggering.
   /// </summary>
   public IObservable<object?> AnyChanged => _anyChanged;

   /// <summary>
   /// Register a string property mapped to an Anki field.
   /// </summary>
   public Property<string> String(string fieldKey)
   {
      return Register(fieldKey, v => v, v => v, "");
   }

   /// <summary>
   /// Register an integer property stored as a string in Anki.
   /// </summary>
   public Property<int> Int(string fieldKey, int defaultValue = 0)
   {
      return Register(fieldKey,
         str => int.TryParse(str, out var v) ? v : defaultValue,
         value => value.ToString(),
         defaultValue);
   }

   /// <summary>
   /// Register a property with custom serialization between T and the Anki string representation.
   /// </summary>
   public Property<T> Register<T>(string fieldKey, Func<string, T> deserialize, Func<T, string> serialize, T defaultValue = default!)
   {
      var property = new Property<T>(defaultValue);
      var registration = new RegisteredProperty<T>(fieldKey, property, serialize, deserialize);
      _properties.Add(registration);
      _subscriptions.Add(property.Subscribe(_ =>
      {
         if (!_isSilent)
         {
            _anyChanged.Fire();
         }
      }));
      return property;
   }

   /// <summary>
   /// Populates all registered properties from an Anki field dictionary.
   /// Uses SetSilently to avoid triggering flushes during deserialization.
   /// </summary>
   public void LoadFromDictionary(Dictionary<string, string>? fields)
   {
      if (fields == null) return;
      _isSilent = true;
      try
      {
         foreach (var registration in _properties)
         {
            if (fields.TryGetValue(registration.FieldKey, out var value))
            {
               registration.DeserializeInto(value);
            }
         }
      }
      finally
      {
         _isSilent = false;
      }
   }

   /// <summary>
   /// Serializes all registered properties to an Anki field dictionary.
   /// Creates a fresh dictionary each time — safe for passing to NoteData.
   /// </summary>
   public Dictionary<string, string> ToDictionary()
   {
      var dict = new Dictionary<string, string>(_properties.Count);
      foreach (var registration in _properties)
      {
         dict[registration.FieldKey] = registration.Serialize();
      }
      return dict;
   }

   /// <summary>
   /// Executes an action with change notifications suppressed.
   /// Useful for batch updates that should only trigger a single flush at the end.
   /// Fires a single AnyChanged notification after the action completes if any registered property was written.
   /// </summary>
   public void Silently(Action action)
   {
      _isSilent = true;
      try
      {
         action();
      }
      finally
      {
         _isSilent = false;
      }
   }

   public void Dispose()
   {
      foreach (var sub in _subscriptions)
      {
         sub.Dispose();
      }
      _subscriptions.Clear();
      _anyChanged.Dispose();
   }

   interface IRegisteredProperty
   {
      string FieldKey { get; }
      void DeserializeInto(string value);
      string Serialize();
   }

   sealed class RegisteredProperty<T> : IRegisteredProperty
   {
      readonly Property<T> _property;
      readonly Func<T, string> _serialize;
      readonly Func<string, T> _deserialize;

      public string FieldKey { get; }

      public RegisteredProperty(string fieldKey, Property<T> property, Func<T, string> serialize, Func<string, T> deserialize)
      {
         FieldKey = fieldKey;
         _property = property;
         _serialize = serialize;
         _deserialize = deserialize;
      }

      public void DeserializeInto(string value)
      {
         _property.SetSilently(_deserialize(value));
      }

      public string Serialize()
      {
         return _serialize(_property.Value);
      }
   }
}
