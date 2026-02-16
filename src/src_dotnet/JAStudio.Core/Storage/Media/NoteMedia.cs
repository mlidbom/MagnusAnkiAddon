using System.Collections.Generic;

namespace JAStudio.Core.Storage.Media;

public record NoteMedia(
   IReadOnlyList<AudioAttachment> Audio,
   IReadOnlyList<ImageAttachment> Images)
{
   public static NoteMedia Empty { get; } = new([], []);
}
