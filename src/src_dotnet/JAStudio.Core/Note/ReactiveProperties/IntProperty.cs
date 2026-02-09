namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// An integer property backed by a <see cref="StringProperty"/>.
/// Replaces IntegerField for PropertyBag-based notes.
/// </summary>
public class IntProperty
{
   readonly StringProperty _field;

   public IntProperty(StringProperty field)
   {
      _field = field;
   }

   public int Get() => _field.HasValue() && int.TryParse(_field.Value, out var v) ? v : 0;

   public void Set(int value) => _field.Set(value.ToString());
}
