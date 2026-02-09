using System;

namespace JAStudio.Core.Note.ReactiveProperties;

public static class ObservableExtensions
{
   /// <summary>
   /// Subscribes to an IObservable with a simple action callback.
   /// </summary>
   public static IDisposable Subscribe<T>(this IObservable<T> source, Action<T> onNext)
   {
      return source.Subscribe(new DelegateObserver<T>(onNext));
   }

   /// <summary>
   /// Subscribes to an IObservable with a parameterless action callback.
   /// </summary>
   public static IDisposable Subscribe<T>(this IObservable<T> source, Action onNext)
   {
      return source.Subscribe(new DelegateObserver<T>(_ => onNext()));
   }

   /// <summary>
   /// Casts an IObservable&lt;T&gt; to IObservable&lt;object?&gt; for use as a Computed source.
   /// This is needed because IObservable is not covariant.
   /// </summary>
   public static IObservable<object?> AsUntyped<T>(this IObservable<T> source)
   {
      return new CastingObservable<T>(source);
   }

   sealed class CastingObservable<T> : IObservable<object?>
   {
      readonly IObservable<T> _source;

      public CastingObservable(IObservable<T> source) => _source = source;

      public IDisposable Subscribe(IObserver<object?> observer)
      {
         return _source.Subscribe(new CastingObserver(observer));
      }

      sealed class CastingObserver : IObserver<T>
      {
         readonly IObserver<object?> _inner;
         public CastingObserver(IObserver<object?> inner) => _inner = inner;
         public void OnNext(T value) => _inner.OnNext(value);
         public void OnError(Exception error) => _inner.OnError(error);
         public void OnCompleted() => _inner.OnCompleted();
      }
   }
}
