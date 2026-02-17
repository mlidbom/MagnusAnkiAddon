namespace JAStudio.Core.Note.NoteFields;

internal class FallbackStringField
{
   readonly IStringValue _field;
   readonly IStringValue _fallbackField;

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
