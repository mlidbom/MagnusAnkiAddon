using System;
using System.Collections.Generic;
using JAStudio.Core.Note;
using MemoryPack;

namespace JAStudio.Core.Storage.Media;

[MemoryPackable]
partial class MediaSnapshotContainer
{
   public List<AudioAttachmentSnapshotData> Audio { get; set; } = [];
   public List<ImageAttachmentSnapshotData> Images { get; set; } = [];
}

[MemoryPackable]
partial class AudioAttachmentSnapshotData
{
   public Guid Id { get; set; }
   public List<Guid> NoteIds { get; set; } = [];
   public string NoteSourceTag { get; set; } = "";
   public string? OriginalFileName { get; set; }
   public CopyrightStatus Copyright { get; set; }
   public string FilePath { get; set; } = "";
   public string? TtsEngine { get; set; }
   public string? TtsVoice { get; set; }
   public string? TtsVersion { get; set; }
}

[MemoryPackable]
partial class ImageAttachmentSnapshotData
{
   public Guid Id { get; set; }
   public List<Guid> NoteIds { get; set; } = [];
   public string NoteSourceTag { get; set; } = "";
   public string? OriginalFileName { get; set; }
   public CopyrightStatus Copyright { get; set; }
   public string FilePath { get; set; } = "";
}

static class MediaSnapshotConverter
{
   public static AudioAttachmentSnapshotData ToSnapshotData(AudioAttachment a) => new()
   {
      Id = a.Id.Value,
      NoteIds = a.NoteIds.ConvertAll(n => n.Value),
      NoteSourceTag = a.NoteSourceTag.ToString(),
      OriginalFileName = a.OriginalFileName,
      Copyright = a.Copyright,
      FilePath = a.FilePath,
      TtsEngine = a.Tts?.Engine,
      TtsVoice = a.Tts?.Voice,
      TtsVersion = a.Tts?.Version,
   };

   public static ImageAttachmentSnapshotData ToSnapshotData(ImageAttachment i) => new()
   {
      Id = i.Id.Value,
      NoteIds = i.NoteIds.ConvertAll(n => n.Value),
      NoteSourceTag = i.NoteSourceTag.ToString(),
      OriginalFileName = i.OriginalFileName,
      Copyright = i.Copyright,
      FilePath = i.FilePath,
   };

   public static AudioAttachment ToAudioAttachment(AudioAttachmentSnapshotData d) => new()
   {
      Id = new MediaFileId(d.Id),
      NoteIds = d.NoteIds.ConvertAll(g => new NoteId(g)),
      NoteSourceTag = SourceTag.Parse(d.NoteSourceTag),
      OriginalFileName = d.OriginalFileName,
      Copyright = d.Copyright,
      FilePath = d.FilePath,
      Tts = d.TtsEngine != null ? new TtsInfo(d.TtsEngine, d.TtsVoice ?? "", d.TtsVersion ?? "") : null,
   };

   public static ImageAttachment ToImageAttachment(ImageAttachmentSnapshotData d) => new()
   {
      Id = new MediaFileId(d.Id),
      NoteIds = d.NoteIds.ConvertAll(g => new NoteId(g)),
      NoteSourceTag = SourceTag.Parse(d.NoteSourceTag),
      OriginalFileName = d.OriginalFileName,
      Copyright = d.Copyright,
      FilePath = d.FilePath,
   };

   public static MediaSnapshotContainer ToContainer(List<MediaAttachment> audioAttachments, List<MediaAttachment> imageAttachments) => new()
   {
      Audio = audioAttachments.ConvertAll(a => ToSnapshotData((AudioAttachment)a)),
      Images = imageAttachments.ConvertAll(i => ToSnapshotData((ImageAttachment)i)),
   };
}
