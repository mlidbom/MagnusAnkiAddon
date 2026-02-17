using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Storage.Media;

public class MediaImportExecutor
{
   readonly MediaStorageService _storageService;
   readonly TaskRunner _taskRunner;

   public MediaImportExecutor(MediaStorageService storageService, TaskRunner taskRunner)
   {
      _storageService = storageService;
      _taskRunner = taskRunner;
   }

   public void Execute(MediaImportPlan plan)
   {
      using var scope = _taskRunner.Current("Importing media from Anki");

      scope.RunBatch(plan.AlreadyStored,
                     alreadyStored =>
                        _storageService.AddNoteIdToExisting(alreadyStored.Existing, alreadyStored.NoteId),
                     "Updating shared file references");

      scope.RunBatch(plan.FilesToImport,
                     file => _storageService.StoreFile(file.SourcePath, file.TargetDirectory, file.SourceTag, file.OriginalFileName, file.NoteId, file.MediaType, file.Copyright),
                     "Copying media files");
   }
}
