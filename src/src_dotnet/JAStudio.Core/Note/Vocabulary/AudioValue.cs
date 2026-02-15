using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class WritableAudioValue
{
   readonly NoteGuard _guard;
   string _value;

   public WritableAudioValue(string initialValue, NoteGuard guard)
   {
      _value = initialValue;
      _guard = guard;
   }

   public string RawValue() => _value;

   public bool HasAudio() => _value.Trim().StartsWith("[sound:");

   public string FirstAudioFilePath() => HasAudio() ? AudioFilesPaths()[0] : string.Empty;

   public List<string> AudioFilesPaths()
   {
      if (!_value.Trim().StartsWith("[sound:")) return [];

      var strippedPaths = _value.Trim().Replace("[sound:", "").Split(']');
      return strippedPaths.Select(path => path.Trim()).Where(path => !string.IsNullOrEmpty(path)).ToList();
   }

   public List<MediaReference> GetMediaReferences() => MediaFieldParsing.ParseAudioReferences(_value);

   public void SetRawValue(string value) => _guard.Update(() => _value = value);

   public override string ToString() => _value;
}
