using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.ReactiveProperties;

/// <summary>
/// Audio field backed by a <see cref="StringProperty"/>.
/// Provides the same API as the old AudioField/WritableAudioField wrappers.
/// </summary>
public class AudioProperty
{
   readonly StringProperty _field;

   public AudioProperty(StringProperty field)
   {
      _field = field;
   }

   public bool HasAudio()
   {
      return _field.Value.Trim().StartsWith("[sound:");
   }

   public string FirstAudioFilePath()
   {
      return HasAudio() ? AudioFilesPaths()[0] : string.Empty;
   }

   public string RawValue()
   {
      return _field.Value;
   }

   public void SetRawValue(string value)
   {
      _field.Set(value);
   }

   public List<string> AudioFilesPaths()
   {
      if (!HasAudio())
      {
         return [];
      }

      var strippedPaths = _field.Value.Trim().Replace("[sound:", "").Split(']');
      return strippedPaths.Select(path => path.Trim()).Where(path => !string.IsNullOrEmpty(path)).ToList();
   }

   public override string ToString() => _field.ToString();
}
