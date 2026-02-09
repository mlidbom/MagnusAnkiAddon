using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.ReactiveProperties;

public class Property<T> : IObservable<T>, IDisposable
{
   T _value;
   List<Subscription>? _observers;
   bool _disposed;

   public Property(T initialValue = default!)
   {
      _value = initialValue;
   }

   public T Value
   {
      get => _value;
      set
      {
         if (EqualityComparer<T>.Default.Equals(_value, value)) return;
         _value = value;
         NotifyObservers();
      }
   }

   /// <summary>
   /// Sets the value without notifying observers or triggering any side effects.
   /// Use this exclusively for deserialization from Anki boundary data.
   /// </summary>
   public void SetSilently(T value)
   {
      _value = value;
   }

   public IDisposable Subscribe(IObserver<T> observer)
   {
      if (_disposed) throw new ObjectDisposedException(nameof(Property<T>));
      _observers ??= [];
      var subscription = new Subscription(this, observer);
      _observers.Add(subscription);
      return subscription;
   }

   void NotifyObservers()
   {
      if (_observers == null) return;
      // Iterate a snapshot to allow subscriptions/unsubscriptions during notification
      var count = _observers.Count;
      for (var i = 0; i < count && i < _observers.Count; i++)
      {
         _observers[i].Observer.OnNext(_value);
      }
   }

   void RemoveObserver(Subscription subscription)
   {
      _observers?.Remove(subscription);
   }

   public void Dispose()
   {
      if (_disposed) return;
      _disposed = true;
      if (_observers != null)
      {
         foreach (var subscription in _observers)
         {
            subscription.Observer.OnCompleted();
         }
         _observers.Clear();
         _observers = null;
      }
   }

   public override string ToString() => _value?.ToString() ?? "";

   sealed class Subscription : IDisposable
   {
      readonly Property<T> _property;
      public IObserver<T> Observer { get; }

      public Subscription(Property<T> property, IObserver<T> observer)
      {
         _property = property;
         Observer = observer;
      }

      public void Dispose()
      {
         _property.RemoveObserver(this);
      }
   }
}

internal sealed class DelegateObserver<T> : IObserver<T>
{
   readonly Action<T> _onNext;
   readonly Action<Exception>? _onError;
   readonly Action? _onCompleted;

   public DelegateObserver(Action<T> onNext, Action<Exception>? onError = null, Action? onCompleted = null)
   {
      _onNext = onNext;
      _onError = onError;
      _onCompleted = onCompleted;
   }

   public void OnNext(T value) => _onNext(value);
   public void OnError(Exception error) => _onError?.Invoke(error);
   public void OnCompleted() => _onCompleted?.Invoke();
}
