using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// A comma-separated list backed by a <see cref="StringProperty"/>.
/// Replaces MutableCommaSeparatedStringsListField for PropertyBag-based notes.
/// Supports lazy cached readers that invalidate on write.
/// </summary>
public class CommaSeparatedListProperty
{
   readonly StringProperty _field;
   List<Action>? _resetCallbacks;
   List<string>? _cached;

   public CommaSeparatedListProperty(StringProperty field)
   {
      _field = field;
   }

   List<string> Parse()
   {
      var value = _field.Value;
      if (string.IsNullOrWhiteSpace(value)) return [];

      return value.Split(',')
         .Select(s => s.Trim())
         .Where(s => !string.IsNullOrEmpty(s))
         .ToList();
   }

   public List<string> Get()
   {
      return _cached ??= Parse();
   }

   public virtual void Set(List<string> value)
   {
      _cached = null;
      InvalidateLazyReaders();
      _field.Set(string.Join(", ", value));
   }

   public void Remove(string remove)
   {
      Set(Get().Where(item => item != remove).ToList());
   }

   public void Add(string add)
   {
      var current = Get();
      current.Add(add);
      Set(current);
   }

   public string RawStringValue() => _field.Value;

   /// <summary>
   /// Register a lazily computed value that resets when the field changes.
   /// Same pattern as CachingMutableStringField.LazyReader.
   /// </summary>
   public Compze.Utilities.SystemCE.LazyCE<T> LazyReader<T>(Func<T> reader) where T : class
   {
      var lazy = new Compze.Utilities.SystemCE.LazyCE<T>(reader);
      _resetCallbacks ??= [];
      _resetCallbacks.Add(lazy.Reset);
      return lazy;
   }

   void InvalidateLazyReaders()
   {
      if (_resetCallbacks == null) return;
      foreach (var cb in _resetCallbacks) cb();
   }

   public override string ToString() => string.Join(", ", Get());
}

/// <summary>
/// A <see cref="CommaSeparatedListProperty"/> that deduplicates on write.
/// Replaces MutableCommaSeparatedStringsListFieldDeDuplicated.
/// </summary>
public class DeDuplicatedCommaSeparatedListProperty : CommaSeparatedListProperty
{
   public DeDuplicatedCommaSeparatedListProperty(StringProperty field) : base(field) { }

   public override void Set(List<string> value) => base.Set(value.Distinct().ToList());
}
