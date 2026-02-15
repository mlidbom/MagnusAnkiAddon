namespace JAStudio.Core.Note.NoteFields;

public interface IStringValue
{
   string Value { get; }
}

public interface IWritableStringValue : IStringValue
{
   void Set(string value);
   bool HasValue();
   void Empty();
}
