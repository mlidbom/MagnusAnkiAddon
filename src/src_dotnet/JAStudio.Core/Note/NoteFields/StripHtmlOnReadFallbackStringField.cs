namespace JAStudio.Core.Note.NoteFields;

public class StripHtmlOnReadFallbackStringField
{
    private readonly FallbackStringField _field;

    public StripHtmlOnReadFallbackStringField(IStringValue primaryField, IStringValue fallbackField)
    {
        _field = new FallbackStringField(primaryField, fallbackField);
    }

    public string Get()
    {
        return StringExtensions.StripHtmlMarkup(_field.Get().Replace("<wbr>", StringExtensions.InvisibleSpace));
    }
}
