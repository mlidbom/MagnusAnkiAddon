using System.Collections.Generic;
using System.Text.Json.Serialization;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage.Media;

public abstract class MediaAttachment
{
   public required MediaFileId Id { get; init; }
   public required List<NoteId> NoteIds { get; init; }
   public required SourceTag NoteSourceTag { get; init; }
   public string? OriginalFileName { get; init; }
   public CopyrightStatus Copyright { get; init; } = CopyrightStatus.Unknown;

   [JsonIgnore] public string FilePath { get; internal set; } = string.Empty;
}

public class AudioAttachment : MediaAttachment
{
   public TtsInfo? Tts { get; init; }
}

public class ImageAttachment : MediaAttachment;
