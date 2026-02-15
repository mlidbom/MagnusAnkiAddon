namespace JAStudio.Core.Note.NoteFields;

public interface IObjectSerializer<T>
{
   string Serialize(T instance);
   T Deserialize(string serialized);
}
