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

   protected IServiceLocator ServiceLocator => TemporaryServiceCollection.Instance.ServiceLocator;
}

public abstract class TestStartingWithEmptyCollection : CollectionUsingTest
{
       protected TestStartingWithEmptyCollection() : base(DataNeeded.None) { }
}