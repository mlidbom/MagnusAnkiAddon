using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core;

/// <summary>
/// Loads backend-specific data (ID mappings and studying statuses) from the host system.
/// Implemented by the integration layer (e.g. JAStudio.Anki).
/// </summary>
public interface IBackendDataLoader
{
   BackendData Load(TaskRunner taskRunner);
}

/// <summary>
/// No-op implementation for tests and environments without a backend data source.
/// Returns empty mappings and statuses.
/// </summary>
class NoOpBackendDataLoader : IBackendDataLoader
{
   public BackendData Load(TaskRunner taskRunner) => new([], []);
}

/// <summary>
/// Data loaded from the backend system that is needed to fully populate caches.
/// Contains the mapping between external IDs and domain NoteIds,
/// plus per-card studying status information.
/// </summary>
public class BackendData
{
   public Dictionary<long, NoteId> IdMappings { get; }
   public List<CardStudyingStatus> StudyingStatuses { get; }

   public BackendData(Dictionary<long, NoteId> idMappings, List<CardStudyingStatus> studyingStatuses)
   {
      IdMappings = idMappings;
      StudyingStatuses = studyingStatuses;
   }
}
