namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// A <see cref="Property{T}"/> specialized for strings with convenience methods
/// matching the old MutableStringField API: Set(), HasValue(), Empty().
/// This minimizes changes at call sites during migration.
/// </summary>
public class StringProperty : Property<string>
{
   public StringProperty(string initialValue = "") : base(initialValue) { }

   public void Set(string value) => Value = value;

   public bool HasValue() => !string.IsNullOrEmpty(Value);

   public void Empty() => Value = string.Empty;
}
