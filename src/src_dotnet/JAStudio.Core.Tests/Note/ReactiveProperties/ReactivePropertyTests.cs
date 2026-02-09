using System;
using System.Collections.Generic;
using JAStudio.Core.Note.ReactiveProperties;
using Xunit;

namespace JAStudio.Core.Tests.Note.ReactiveProperties;

public class PropertyTests
{
   [Fact]
   public void InitialValue_IsAvailable()
   {
      var prop = new Property<string>("hello");
      Assert.Equal("hello", prop.Value);
   }

   [Fact]
   public void DefaultInitialValue_IsDefault()
   {
      var prop = new Property<int>();
      Assert.Equal(0, prop.Value);
   }

   [Fact]
   public void Set_UpdatesValue()
   {
      var prop = new Property<string>("a");
      prop.Value = "b";
      Assert.Equal("b", prop.Value);
   }

   [Fact]
   public void Set_NotifiesSubscribers()
   {
      var prop = new Property<string>("a");
      var received = new List<string>();
      prop.Subscribe(v => received.Add(v));

      prop.Value = "b";
      prop.Value = "c";

      Assert.Equal(["b", "c"], received);
   }

   [Fact]
   public void Set_SameValue_DoesNotNotify()
   {
      var prop = new Property<string>("a");
      var notifyCount = 0;
      prop.Subscribe(_ => notifyCount++);

      prop.Value = "a";

      Assert.Equal(0, notifyCount);
   }

   [Fact]
   public void SetSilently_UpdatesValue_WithoutNotifying()
   {
      var prop = new Property<string>("a");
      var notifyCount = 0;
      prop.Subscribe(_ => notifyCount++);

      prop.SetSilently("b");

      Assert.Equal("b", prop.Value);
      Assert.Equal(0, notifyCount);
   }

   [Fact]
   public void MultipleSubscribers_AllNotified()
   {
      var prop = new Property<int>(0);
      var received1 = new List<int>();
      var received2 = new List<int>();
      prop.Subscribe(v => received1.Add(v));
      prop.Subscribe(v => received2.Add(v));

      prop.Value = 42;

      Assert.Equal([42], received1);
      Assert.Equal([42], received2);
   }

   [Fact]
   public void Unsubscribe_StopsNotifications()
   {
      var prop = new Property<string>("a");
      var received = new List<string>();
      var sub = prop.Subscribe(v => received.Add(v));

      prop.Value = "b";
      sub.Dispose();
      prop.Value = "c";

      Assert.Equal(["b"], received);
   }

   [Fact]
   public void Dispose_CompletesObservers()
   {
      var prop = new Property<string>("a");
      var completed = false;
      prop.Subscribe(new TestObserver<string>(onCompleted: () => completed = true));

      prop.Dispose();

      Assert.True(completed);
   }

   [Fact]
   public void Dispose_StopsAllNotifications()
   {
      var prop = new Property<string>("a");
      var notifyCount = 0;
      prop.Subscribe(_ => notifyCount++);

      prop.Dispose();
      Assert.Throws<ObjectDisposedException>(() => prop.Subscribe(_ => { }));
   }

   [Fact]
   public void Subscribe_WithActionOverload()
   {
      var prop = new Property<string>("a");
      var called = false;
      prop.Subscribe(() => called = true);

      prop.Value = "b";

      Assert.True(called);
   }

   [Fact]
   public void ToString_ReturnsValueString()
   {
      var prop = new Property<int>(42);
      Assert.Equal("42", prop.ToString());
   }

   [Fact]
   public void ToString_NullValue_ReturnsEmpty()
   {
      var prop = new Property<string?>(null);
      Assert.Equal("", prop.ToString());
   }

   [Fact]
   public void NullableReferenceType_Works()
   {
      var prop = new Property<string?>(null);
      Assert.Null(prop.Value);
      prop.Value = "hello";
      Assert.Equal("hello", prop.Value);
      prop.Value = null;
      Assert.Null(prop.Value);
   }
}

public class ComputedTests
{
   [Fact]
   public void InitialValue_IsComputed()
   {
      var a = new Property<string>("hello");
      var computed = new Computed<string>(() => a.Value.ToUpperInvariant(), a.AsUntyped());

      Assert.Equal("HELLO", computed.Value);
   }

   [Fact]
   public void Recomputes_WhenSourceChanges()
   {
      var a = new Property<string>("hello");
      var computed = new Computed<string>(() => a.Value.ToUpperInvariant(), a.AsUntyped());

      a.Value = "world";

      Assert.Equal("WORLD", computed.Value);
   }

   [Fact]
   public void MultipleSources_RecomputesOnAnyChange()
   {
      var first = new Property<string>("John");
      var last = new Property<string>("Doe");
      var fullName = new Computed<string>(
         () => $"{first.Value} {last.Value}",
         first.AsUntyped(), last.AsUntyped());

      Assert.Equal("John Doe", fullName.Value);

      first.Value = "Jane";
      Assert.Equal("Jane Doe", fullName.Value);

      last.Value = "Smith";
      Assert.Equal("Jane Smith", fullName.Value);
   }

   [Fact]
   public void NotifiesSubscribers_WhenValueChanges()
   {
      var source = new Property<int>(1);
      var doubled = new Computed<int>(() => source.Value * 2, source.AsUntyped());
      var received = new List<int>();
      doubled.Subscribe(v => received.Add(v));

      source.Value = 5;
      source.Value = 10;

      Assert.Equal([10, 20], received);
   }

   [Fact]
   public void DoesNotNotify_WhenComputedValueUnchanged()
   {
      var source = new Property<int>(3);
      var isPositive = new Computed<bool>(() => source.Value > 0, source.AsUntyped());
      var notifyCount = 0;
      isPositive.Subscribe(_ => notifyCount++);

      source.Value = 5; // still positive — no notification
      source.Value = 100; // still positive — no notification

      Assert.Equal(0, notifyCount);
   }

   [Fact]
   public void FallbackPattern_UserOverridesSource()
   {
      var userAnswer = new Property<string>("");
      var sourceAnswer = new Property<string>("source");
      var activeAnswer = new Computed<string>(
         () => !string.IsNullOrEmpty(userAnswer.Value) ? userAnswer.Value : sourceAnswer.Value,
         userAnswer.AsUntyped(), sourceAnswer.AsUntyped());

      Assert.Equal("source", activeAnswer.Value);

      userAnswer.Value = "user override";
      Assert.Equal("user override", activeAnswer.Value);

      userAnswer.Value = "";
      Assert.Equal("source", activeAnswer.Value);
   }

   [Fact]
   public void Dispose_UnsubscribesFromSources()
   {
      var source = new Property<int>(1);
      var doubled = new Computed<int>(() => source.Value * 2, source.AsUntyped());

      doubled.Dispose();
      source.Value = 5;

      // Computed should not have recomputed after dispose
      Assert.Equal(2, doubled.Value);
   }

   [Fact]
   public void ChainingComputed_Works()
   {
      var a = new Property<int>(2);
      var doubled = new Computed<int>(() => a.Value * 2, a.AsUntyped());
      var quadrupled = new Computed<int>(() => doubled.Value * 2, doubled.AsUntyped());

      Assert.Equal(8, quadrupled.Value);

      a.Value = 3;
      Assert.Equal(12, quadrupled.Value);
   }
}

public class PropertyBagTests
{
   [Fact]
   public void RegisterString_DefaultsToEmpty()
   {
      using var bag = new PropertyBag();
      var prop = bag.String("Q");
      Assert.Equal("", prop.Value);
   }

   [Fact]
   public void LoadFromDictionary_PopulatesProperties()
   {
      using var bag = new PropertyBag();
      var q = bag.String("Q");
      var a = bag.String("A");

      bag.LoadFromDictionary(new Dictionary<string, string>
      {
         ["Q"] = "question text",
         ["A"] = "answer text"
      });

      Assert.Equal("question text", q.Value);
      Assert.Equal("answer text", a.Value);
   }

   [Fact]
   public void LoadFromDictionary_DoesNotTriggerAnyChanged()
   {
      using var bag = new PropertyBag();
      var q = bag.String("Q");
      var notifyCount = 0;
      bag.AnyChanged.Subscribe(_ => notifyCount++);

      bag.LoadFromDictionary(new Dictionary<string, string> { ["Q"] = "test" });

      Assert.Equal(0, notifyCount);
   }

   [Fact]
   public void LoadFromDictionary_NullFields_DoesNotThrow()
   {
      using var bag = new PropertyBag();
      var q = bag.String("Q");

      bag.LoadFromDictionary(null);

      Assert.Equal("", q.Value);
   }

   [Fact]
   public void LoadFromDictionary_MissingKey_KeepsDefault()
   {
      using var bag = new PropertyBag();
      var q = bag.String("Q");
      var a = bag.String("A");

      bag.LoadFromDictionary(new Dictionary<string, string> { ["Q"] = "test" });

      Assert.Equal("test", q.Value);
      Assert.Equal("", a.Value);
   }

   [Fact]
   public void ToDictionary_SerializesAllProperties()
   {
      using var bag = new PropertyBag();
      var q = bag.String("Q");
      var a = bag.String("A");

      q.Value = "question";
      a.Value = "answer";

      var dict = bag.ToDictionary();

      Assert.Equal("question", dict["Q"]);
      Assert.Equal("answer", dict["A"]);
   }

   [Fact]
   public void ToDictionary_ProducesNewDictionaryEachCall()
   {
      using var bag = new PropertyBag();
      bag.String("Q");

      var dict1 = bag.ToDictionary();
      var dict2 = bag.ToDictionary();

      Assert.NotSame(dict1, dict2);
   }

   [Fact]
   public void IntProperty_RoundTrips()
   {
      using var bag = new PropertyBag();
      var count = bag.Int("count");

      count.Value = 42;
      var dict = bag.ToDictionary();
      Assert.Equal("42", dict["count"]);

      using var bag2 = new PropertyBag();
      var count2 = bag2.Int("count");
      bag2.LoadFromDictionary(dict);
      Assert.Equal(42, count2.Value);
   }

   [Fact]
   public void IntProperty_InvalidString_DefaultsToZero()
   {
      using var bag = new PropertyBag();
      var count = bag.Int("count");

      bag.LoadFromDictionary(new Dictionary<string, string> { ["count"] = "not_a_number" });

      Assert.Equal(0, count.Value);
   }

   [Fact]
   public void CustomSerialization_RoundTrips()
   {
      using var bag = new PropertyBag();
      var items = bag.Register("items",
         str => str.Length == 0 ? new List<string>() : new List<string>(str.Split(',')),
         list => string.Join(",", list),
         new List<string>());

      items.Value = ["apple", "banana", "cherry"];

      var dict = bag.ToDictionary();
      Assert.Equal("apple,banana,cherry", dict["items"]);

      using var bag2 = new PropertyBag();
      var items2 = bag2.Register("items",
         str => str.Length == 0 ? new List<string>() : new List<string>(str.Split(',')),
         list => string.Join(",", list),
         new List<string>());
      bag2.LoadFromDictionary(dict);
      Assert.Equal(["apple", "banana", "cherry"], items2.Value);
   }

   [Fact]
   public void AnyChanged_FiresOnPropertyChange()
   {
      using var bag = new PropertyBag();
      var q = bag.String("Q");
      var a = bag.String("A");
      var notifyCount = 0;
      bag.AnyChanged.Subscribe(_ => notifyCount++);

      q.Value = "changed";
      Assert.Equal(1, notifyCount);

      a.Value = "also changed";
      Assert.Equal(2, notifyCount);
   }

   [Fact]
   public void Silently_SuppressesAnyChanged()
   {
      using var bag = new PropertyBag();
      var q = bag.String("Q");
      var a = bag.String("A");
      var notifyCount = 0;
      bag.AnyChanged.Subscribe(_ => notifyCount++);

      bag.Silently(() =>
      {
         q.Value = "changed";
         a.Value = "also changed";
      });

      Assert.Equal(0, notifyCount);
      Assert.Equal("changed", q.Value);
      Assert.Equal("also changed", a.Value);
   }

   [Fact]
   public void FullRoundTrip_LoadModifySerialize()
   {
      using var bag = new PropertyBag();
      var q = bag.String("Q");
      var a = bag.String("A");
      var count = bag.Int("count");

      // Load from Anki
      bag.LoadFromDictionary(new Dictionary<string, string>
      {
         ["Q"] = "original question",
         ["A"] = "original answer",
         ["count"] = "5"
      });

      Assert.Equal("original question", q.Value);
      Assert.Equal("original answer", a.Value);
      Assert.Equal(5, count.Value);

      // Modify
      q.Value = "updated question";
      count.Value = 10;

      // Serialize back
      var dict = bag.ToDictionary();
      Assert.Equal("updated question", dict["Q"]);
      Assert.Equal("original answer", dict["A"]);
      Assert.Equal("10", dict["count"]);
   }
}

/// <summary>
/// Helper observer for tests that need fine-grained control.
/// </summary>
sealed class TestObserver<T> : IObserver<T>
{
   readonly Action<T>? _onNext;
   readonly Action<Exception>? _onError;
   readonly Action? _onCompleted;

   public TestObserver(Action<T>? onNext = null, Action<Exception>? onError = null, Action? onCompleted = null)
   {
      _onNext = onNext;
      _onError = onError;
      _onCompleted = onCompleted;
   }

   public void OnNext(T value) => _onNext?.Invoke(value);
   public void OnError(Exception error) => _onError?.Invoke(error);
   public void OnCompleted() => _onCompleted?.Invoke();
}
