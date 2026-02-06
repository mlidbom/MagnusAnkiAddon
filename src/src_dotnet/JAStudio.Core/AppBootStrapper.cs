using Compze.Utilities.DependencyInjection;
using Compze.Utilities.DependencyInjection.Abstractions;
using Compze.Utilities.DependencyInjection.SimpleInjector;
using JAStudio.Core.AnkiUtils;

namespace JAStudio.Core;

static class AppBootstrapper
{
   public static App Bootstrap()
   {
      var container = new SimpleInjectorDependencyInjectionContainer();
      var registrar = container.Register();

      registrar.Register(
         Singleton.For<TemporaryServiceLocator>().CreatedBy(() => new TemporaryServiceLocator(container.ServiceLocator)),
         Singleton.For<App>().CreatedBy((TemporaryServiceLocator services) => new App(services)),
         Singleton.For<QueryBuilder>().CreatedBy((TemporaryServiceLocator services) => new QueryBuilder(services))
      );

      return container.ServiceLocator.Resolve<App>();
   }
}