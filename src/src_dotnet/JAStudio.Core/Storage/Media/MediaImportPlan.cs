using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Storage.Media;

public record PlannedFileImport(
   string SourcePath,
   string TargetDirectory,
   CopyrightStatus Copyright,
   SourceTag SourceTag,
   string OriginalFileName,
   NoteId NoteId,
   MediaType MediaType);

public record AlreadyStoredFile(MediaAttachment Existing, NoteId NoteId);

public record MissingFile(string FileName, NoteId NoteId);

public class MediaImportPlan
{
   public List<PlannedFileImport> FilesToImport { get; } = [];
   public List<AlreadyStoredFile> AlreadyStored { get; } = [];
   public List<MissingFile> Missing { get; } = [];
}
