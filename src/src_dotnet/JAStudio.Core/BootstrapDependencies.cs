using System;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core;

/// <summary>
/// All host-specific dependencies needed to bootstrap the application.
/// Implemented by the Anki addon runtime and by the test harness.
/// </summary>
public interface IBootstrapDependencies
{
   IEnvironmentPaths EnvironmentPaths { get; }
   IBackendNoteCreator BackendNoteCreator { get; }
   IBackendDataLoader? BackendDataLoader { get; }
   IFatalErrorHandler FatalErrorHandler { get; }
   ITaskProgressUI TaskProgressUI { get; }
   IConfigDictSource ConfigDictSource { get; }
   IReadingsMappingsSource? ReadingsMappingsSource { get; }
   Func<ExternalNoteIdMap, ICardOperations> CardOperationsFactory { get; }
}
