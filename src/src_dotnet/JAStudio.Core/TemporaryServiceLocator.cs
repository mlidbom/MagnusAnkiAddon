using System;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.AnkiUtils;

namespace JAStudio.Core;

//TODO: We should redesign so that we have a sane dependency graph and just use normal dependency injection, but first we need to get rid of all the static classes and this will help us do that
class TemporaryServiceLocator(IServiceLocator serviceLocator) : IDisposable
{
   readonly IServiceLocator _serviceLocator = serviceLocator;
   public App App => _serviceLocator.Resolve<App>();
   public QueryBuilder QueryBuilder => _serviceLocator.Resolve<QueryBuilder>();

   public void Dispose() => _serviceLocator.Dispose();
}
