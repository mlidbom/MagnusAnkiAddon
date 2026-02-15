using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class AudioValue
{
   readonly Func<string> _getValue;

   public AudioValue(Func<string> getValue) => _getValue = getValue;

   public string RawValue() => _getValue();

   public bool HasAudio() => _getValue().Trim().StartsWith("[sound:");

   public string FirstAudioFilePath() => HasAudio() ? AudioFilesPaths()[0] : string.Empty;

   public List<string> AudioFilesPaths()
   {
      var value = _getValue();
      if (!value.Trim().StartsWith("[sound:")) return [];

      var strippedPaths = value.Trim().Replace("[sound:", "").Split(']');
      return strippedPaths.Select(path => path.Trim()).Where(path => !string.IsNullOrEmpty(path)).ToList();
   }

   public List<MediaReference> GetMediaReferences() => MediaFieldParsing.ParseAudioReferences(_getValue());

   public override string ToString() => _getValue();
}

public class WritableAudioValue : AudioValue
{
   readonly Action<string> _setValue;

   public WritableAudioValue(Func<string> getValue, Action<string> setValue) : base(getValue) => _setValue = setValue;

   public void SetRawValue(string value) => _setValue(value);
}
