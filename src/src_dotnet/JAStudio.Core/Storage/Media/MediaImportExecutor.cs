namespace JAStudio.Core.Storage.Media;

public class MediaImportExecutor
{
   readonly MediaStorageService _storageService;

   public MediaImportExecutor(MediaStorageService storageService)
   {
      _storageService = storageService;
   }

   public void Execute(MediaImportPlan plan)
   {
      foreach(var alreadyStored in plan.AlreadyStored)
      {
         _storageService.AddNoteIdToExisting(alreadyStored.Existing, alreadyStored.NoteId);
      }

      foreach(var file in plan.FilesToImport)
      {
         _storageService.StoreFile(file.SourcePath, file.TargetDirectory, file.SourceTag, file.OriginalFileName, file.NoteId, file.MediaType, file.Copyright);
      }
   }
}
