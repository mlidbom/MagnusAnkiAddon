using System.Collections.Generic;

namespace JAStudio.Core.Storage.Media;

public class NoteMedia(IReadOnlyList<AudioAttachment> audio, IReadOnlyList<ImageAttachment> images)
{
   public static NoteMedia Empty { get; } = new([], []);

   public IReadOnlyList<AudioAttachment> Audio { get; } = audio;
   public IReadOnlyList<ImageAttachment> Images { get; } = images;
}
