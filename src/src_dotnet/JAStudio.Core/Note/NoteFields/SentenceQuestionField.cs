namespace JAStudio.Core.Note.NoteFields;

public class SentenceQuestionField
{
    public const string WordBreakTag = "<wbr>";
    
    private readonly MutableStringField _userField;
    private readonly MutableStringField _sourceField;

    public SentenceQuestionField(MutableStringField primaryField, MutableStringField fallbackField)
    {
        _userField = primaryField;
        _sourceField = fallbackField;
    }

    private string SentenceQuestionFieldRawValue()
    {
        return _userField.Value ?? _sourceField.Value;
    }

    public string WithInvisibleSpace()
    {
        return StringExtensions.StripHtmlMarkup(
            SentenceQuestionFieldRawValue().Replace(WordBreakTag, StringExtensions.InvisibleSpace));
    }

    public string WithoutInvisibleSpace()
    {
        return WithInvisibleSpace().Replace(StringExtensions.InvisibleSpace, string.Empty);
    }

    public void SplitTokenWithWordBreakTag(string section)
    {
        if (section.Length < 2)
        {
            return;
        }

        var rawValue = SentenceQuestionFieldRawValue();
        var newSection = $"{section[0]}{WordBreakTag}{section.Substring(1)}";
        var newValue = rawValue.Replace(section, newSection);

        if (_userField.HasValue())
        {
            _userField.Set(newValue);
        }
        else
        {
            _sourceField.Set(newValue);
        }
    }
}
