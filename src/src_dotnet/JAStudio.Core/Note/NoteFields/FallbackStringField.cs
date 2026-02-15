namespace JAStudio.Core.Note.NoteFields;

public class FallbackStringField
{
    private readonly IStringValue _field;
    private readonly IStringValue _fallbackField;

    public FallbackStringField(IStringValue primaryField, IStringValue fallbackField)
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
