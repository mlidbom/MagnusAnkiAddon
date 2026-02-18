using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Storage.Media;

namespace JAStudio.Web;

/// <summary>
/// Selects the best audio attachment from a note's media.
/// Priority: commercial > free non-TTS > TTS.
/// </summary>
static class AudioSelector
{
   public static AudioAttachment? SelectBest(IReadOnlyList<AudioAttachment> audio)
   {
      if(audio.Count == 0) return null;

      // 1. First commercial
      var commercial = audio.FirstOrDefault(a => a.Copyright == CopyrightStatus.Commercial);
      if(commercial != null) return commercial;

      // 2. First free human (non-TTS)
      var freeHuman = audio.FirstOrDefault(a => a.Copyright == CopyrightStatus.Free && a.Tts == null);
      if(freeHuman != null) return freeHuman;

      // 3. First TTS
      var tts = audio.FirstOrDefault(a => a.Tts != null);
      if(tts != null) return tts;

      // 4. Anything remaining
      return audio[0];
   }
}
