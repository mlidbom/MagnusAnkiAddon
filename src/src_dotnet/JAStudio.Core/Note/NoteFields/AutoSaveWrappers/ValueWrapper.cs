namespace JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

public class ValueWrapper<TValue>
{
   TValue _value;

   public ValueWrapper(TValue value) => _value = value;

   public void Set(TValue value)
   {
      _value = value;
   }

   public TValue Get() => _value;

   public override string ToString() => _value?.ToString() ?? string.Empty;
}
