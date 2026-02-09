using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// A read-only property whose value is derived from one or more source observables.
/// Recomputes automatically whenever any source changes.
/// </summary>
public class Computed<T> : IObservable<T>, IDisposable
{
   T _cachedValue;
   readonly Func<T> _compute;
   readonly List<IDisposable> _sourceSubscriptions;
   List<Subscription>? _observers;
   bool _disposed;

   public Computed(Func<T> compute, params IObservable<object?>[] sources)
      : this(compute, (IEnumerable<IObservable<object?>>)sources) { }

   public Computed(Func<T> compute, IEnumerable<IObservable<object?>> sources)
   {
      _compute = compute;
      _sourceSubscriptions = [];
      foreach (var source in sources)
      {
         _sourceSubscriptions.Add(source.Subscribe(new DelegateObserver<object?>(_ => Recompute())));
      }
      _cachedValue = compute();
   }

   public T Value => _cachedValue;

   void Recompute()
   {
      var newValue = _compute();
      if (EqualityComparer<T>.Default.Equals(_cachedValue, newValue)) return;
      _cachedValue = newValue;
      NotifyObservers();
   }

   public IDisposable Subscribe(IObserver<T> observer)
   {
      if (_disposed) throw new ObjectDisposedException(nameof(Computed<T>));
      _observers ??= [];
      var subscription = new Subscription(this, observer);
      _observers.Add(subscription);
      return subscription;
   }

   void NotifyObservers()
   {
      if (_observers == null) return;
      var count = _observers.Count;
      for (var i = 0; i < count && i < _observers.Count; i++)
      {
         _observers[i].Observer.OnNext(_cachedValue);
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
      foreach (var sub in _sourceSubscriptions)
      {
         sub.Dispose();
      }
      _sourceSubscriptions.Clear();
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

   public override string ToString() => _cachedValue?.ToString() ?? "";

   sealed class Subscription : IDisposable
   {
      readonly Computed<T> _computed;
      public IObserver<T> Observer { get; }

      public Subscription(Computed<T> computed, IObserver<T> observer)
      {
         _computed = computed;
         Observer = observer;
      }

      public void Dispose()
      {
         _computed.RemoveObserver(this);
      }
   }
}
