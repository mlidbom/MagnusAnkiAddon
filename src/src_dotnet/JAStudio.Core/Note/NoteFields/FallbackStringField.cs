namespace JAStudio.Core.Note.NoteFields;

public class FallbackStringField
{
    private readonly MutableStringField _field;
    private readonly MutableStringField _fallbackField;

    public FallbackStringField(MutableStringField primaryField, MutableStringField fallbackField)
    {
        _field = primaryField;
        _fallbackField = fallbackField;
    }

    public string Get()
    {
        var primary = _field.Value;
        return !string.IsNullOrEmpty(primary) ? primary : _fallbackField.Value;
    }
}
