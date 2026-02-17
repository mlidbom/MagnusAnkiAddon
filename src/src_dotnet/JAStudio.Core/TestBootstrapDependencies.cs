using System;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core;

class TestBootstrapDependencies : IBootstrapDependencies
{
   public IEnvironmentPaths EnvironmentPaths { get; } = new TestEnvironmentPaths();
   public IBackendNoteCreator BackendNoteCreator { get; } = new TestingBackendNoteCreator();
   public IBackendDataLoader BackendDataLoader { get; } = new NoOpBackendDataLoader();
   public IFatalErrorHandler FatalErrorHandler { get; } = new RethrowingFatalErrorHandler();
   public ITaskProgressUI TaskProgressUI { get; } = new HeadlessTaskProgressUI();
   public IConfigDictSource ConfigDictSource { get; } = new TestConfigDictSource();
   public IReadingsMappingsSource ReadingsMappingsSource { get; } = new TestReadingsMappingsSource();
   public Func<ExternalNoteIdMap, ICardOperations> CardOperationsFactory => _ => new NoOpCardOperations();
}
