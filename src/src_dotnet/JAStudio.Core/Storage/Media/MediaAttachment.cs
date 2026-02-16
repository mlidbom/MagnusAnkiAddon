using System.Collections.Generic;
using System.Text.Json.Serialization;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage.Media;

public abstract record MediaAttachment
{
   public required MediaFileId Id { get; init; }
   public required List<NoteId> NoteIds { get; init; }
   public required string NoteSourceTag { get; init; }
   public string? AnkiFieldName { get; init; }
   public string? OriginalFileName { get; init; }
   public required CopyrightStatus Copyright { get; init; }

   [JsonIgnore] public string FilePath { get; internal set; } = string.Empty;
}

public record AudioAttachment : MediaAttachment
{
   public TtsInfo? Tts { get; init; }
}

public record ImageAttachment : MediaAttachment;
