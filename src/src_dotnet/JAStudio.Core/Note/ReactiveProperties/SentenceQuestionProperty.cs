namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// Computed sentence question with fallback (user → source) and word-break tag support.
/// Replaces SentenceQuestionField for PropertyBag-based notes.
/// </summary>
public class SentenceQuestionProperty
{
   public const string WordBreakTag = "<wbr>";

   readonly StringProperty _userField;
   readonly StringProperty _sourceField;

   public SentenceQuestionProperty(StringProperty userField, StringProperty sourceField)
   {
      _userField = userField;
      _sourceField = sourceField;
   }

   string RawValue()
   {
      var userValue = _userField.Value;
      return string.IsNullOrEmpty(userValue) ? _sourceField.Value : userValue;
   }

   public string WithInvisibleSpace()
   {
      return StringExtensions.StripHtmlMarkup(
         RawValue().Replace(WordBreakTag, StringExtensions.InvisibleSpace));
   }

   public string WithoutInvisibleSpace()
   {
      return WithInvisibleSpace().Replace(StringExtensions.InvisibleSpace, string.Empty);
   }

   public void SplitTokenWithWordBreakTag(string section)
   {
      if (section.Length < 2) return;

      var rawValue = RawValue();
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
