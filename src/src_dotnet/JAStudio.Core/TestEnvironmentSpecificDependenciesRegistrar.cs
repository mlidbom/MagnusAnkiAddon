using Compze.Utilities.DependencyInjection;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Batches;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core;

class TestEnvironmentSpecificDependenciesRegistrar : IEnvironmentSpecificDependenciesRegistrar
{
   public void WireEnvironmentSpecificServices(IComponentRegistrar registrar)
   {
      var paths = new TestEnvironmentPaths();

      registrar.Register(
         Singleton.For<IEnvironmentPaths>().Instance(paths),
         Singleton.For<IBackendNoteCreator>().Instance(new TestingBackendNoteCreator()),
         Singleton.For<IBackendDataLoader>().Instance(new NoOpBackendDataLoader()),
         Singleton.For<IFatalErrorHandler>().Instance(new RethrowingFatalErrorHandler()),
         Singleton.For<IUIThreadDispatcher>().Instance(new HeadlessUIThreadDispatcher()),
         Singleton.For<IConfigDictSource>().Instance(new TestConfigDictSource()),
         Singleton.For<IReadingsMappingsSource>().Instance(new TestReadingsMappingsSource()),
         Singleton.For<ICardOperations>().Instance(new NoOpCardOperations())
      );
   }
}
