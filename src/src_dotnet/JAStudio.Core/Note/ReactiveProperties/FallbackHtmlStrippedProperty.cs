namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// Provides a read-only computed answer string with fallback (user → source), HTML stripping, and
/// word-break tag translation. Replaces StripHtmlOnReadFallbackStringField for PropertyBag-based notes.
/// </summary>
public class FallbackHtmlStrippedProperty
{
   readonly StringProperty _primaryField;
   readonly StringProperty _fallbackField;

   public FallbackHtmlStrippedProperty(StringProperty primaryField, StringProperty fallbackField)
   {
      _primaryField = primaryField;
      _fallbackField = fallbackField;
   }

   public string Get()
   {
      var primary = _primaryField.Value;
      var raw = !string.IsNullOrEmpty(primary) ? primary : _fallbackField.Value;
      return StringExtensions.StripHtmlMarkup(raw.Replace("<wbr>", StringExtensions.InvisibleSpace));
   }
}
