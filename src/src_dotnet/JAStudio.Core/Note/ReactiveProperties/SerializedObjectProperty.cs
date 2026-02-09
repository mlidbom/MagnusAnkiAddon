using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// A serialized object stored as a string in a <see cref="StringProperty"/>.
/// Replaces <see cref="MutableSerializedObjectField{T}"/> for PropertyBag-based notes.
/// </summary>
public class SerializedObjectProperty<T>
{
   readonly StringProperty _field;
   readonly IObjectSerializer<T> _serializer;
   T _value;

   public SerializedObjectProperty(StringProperty field, IObjectSerializer<T> serializer)
   {
      _field = field;
      _serializer = serializer;
      _value = serializer.Deserialize(field.Value);
   }

   public T Get() => _value;

   public void Set(T value)
   {
      _value = value;
      _field.Set(_serializer.Serialize(value));
   }

   public void Save()
   {
      _field.Set(_serializer.Serialize(_value));
   }

   public override string ToString() => Get()?.ToString() ?? string.Empty;
}
