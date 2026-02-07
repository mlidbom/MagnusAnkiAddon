using System;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Tests.Fixtures;

namespace JAStudio.Core.Tests;

public abstract class CollectionUsingTest : IDisposable
{
   protected CollectionUsingTest(DataNeeded data = DataNeeded.All) =>
      _collectionScope = CollectionFactory.InjectCollectionWithSelectData(data);

   public void Dispose() => _collectionScope.Dispose();

   readonly IDisposable _collectionScope;

   protected TService GetService<TService>() where TService : class => TemporaryServiceCollection.Instance.ServiceLocator.Resolve<TService>();
}
