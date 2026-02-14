using JAStudio.Core.Note;

namespace JAStudio.Core.Storage.Media;

public class NullMediaSyncService : IMediaSyncService
{
   public void SyncMedia(JPNote note) { }
}
