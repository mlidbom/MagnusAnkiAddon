using System.Collections.Generic;

namespace JAStudio.Core.Note.NoteFields;

public class ImageField
{
    protected readonly MutableStringField _field;

    public ImageField(MutableStringField field)
    {
        _field = field;
    }

    public bool HasImage() => !string.IsNullOrWhiteSpace(_field.Value) && _field.Value.Contains("<img");

    public string RawValue() => _field.Value;

    public List<string> ImageFilePaths() => MediaFieldParsing.ParseImageReferences(_field.Value)
        .ConvertAll(r => r.FileName);

    public List<MediaReference> GetMediaReferences() => MediaFieldParsing.ParseImageReferences(_field.Value);

    public override string ToString() => _field.ToString();
}

public class WritableImageField : ImageField
{
    public WritableImageField(MutableStringField field) : base(field)
    {
    }

    public void SetRawValue(string value)
    {
        _field.Set(value);
    }
}
