using System.Collections.Generic;

namespace JAStudio.Core.Note.NoteFields;

public class ImageField
{
    protected readonly MutableStringField _field;

    public ImageField(JPNote note, string fieldName)
    {
        _field = new MutableStringField(note, fieldName);
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
    public WritableImageField(JPNote note, string fieldName) : base(note, fieldName)
    {
    }

    public void SetRawValue(string value)
    {
        _field.Set(value);
    }
}
