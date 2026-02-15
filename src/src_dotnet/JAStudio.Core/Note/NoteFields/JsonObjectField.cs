namespace JAStudio.Core.Note.NoteFields;

public interface IObjectSerializer<T>
{
    string Serialize(T instance);
    T Deserialize(string serialized);
}

public class MutableSerializedObjectField<T>
{
    private readonly IObjectSerializer<T> _serializer;
    private readonly MutableStringField _field;
    private T _value;

    public MutableSerializedObjectField(MutableStringField field, IObjectSerializer<T> serializer)
    {
        _serializer = serializer;
        _field = field;
        _value = serializer.Deserialize(_field.Value);
    }

    public T Get() => _value;

    public string RawValue
    {
        get => _field.Value;
        set => _field.Set(value);
    }

    public void Set(T value)
    {
        _value = value;
        _field.Set(_serializer.Serialize(value));
    }

    public void Save()
    {
        _field.Set(_serializer.Serialize(_value));
    }

    public override string ToString()
    {
        return Get()?.ToString() ?? string.Empty;
    }
}
