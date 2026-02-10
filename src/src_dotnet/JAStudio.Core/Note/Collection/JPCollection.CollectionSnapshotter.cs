using System;
using System.Threading;
using Compze.Utilities.Logging;
using JAStudio.Core.Storage;

namespace JAStudio.Core.Note.Collection;

public partial class JPCollection
{
   /// <summary>
   /// Manages periodic and shutdown snapshotting of the note collection to the single-file cache.
   /// Encapsulates the timer, atomic save, and quiet error handling so JPCollection stays focused on domain logic.
   /// </summary>
   class CollectionSnapshotter : IDisposable
   {
      readonly JPCollection _collection;
      Timer? _timer;
      static readonly TimeSpan Interval = TimeSpan.FromMinutes(15);

      internal CollectionSnapshotter(JPCollection collection)
      {
         _collection = collection;
      }

      internal void StartTimer()
      {
         StopTimer();
         if(_collection._noteRepository is not FileSystemNoteRepository) return;
         _timer = new Timer(_ => SaveQuietly(), null, Interval, Interval);
      }

      internal void StopTimer()
      {
         _timer?.Dispose();
         _timer = null;
      }

      void SaveQuietly()
      {
         try
         {
            Save();
         }
         catch(Exception ex)
         {
            _collection.Log().Error(ex, "Snapshot save failed");
         }
      }

      /// <summary>Atomically writes a snapshot of all notes to the single-file cache for fast subsequent loads.</summary>
      void Save()
      {
         using var _ = _collection.Log().Info().LogMethodExecutionTime();
         if(_collection._noteRepository is not FileSystemNoteRepository fileRepo) return;
         var allData = new AllNotesData(_collection.Kanji.All(), _collection.Vocab.All(), _collection.Sentences.All());
         fileRepo.SaveSnapshot(allData);
      }

      public void Dispose()
      {
         StopTimer();
      }
   }
}
