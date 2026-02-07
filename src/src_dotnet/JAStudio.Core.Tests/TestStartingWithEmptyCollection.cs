using JAStudio.Core.Tests.Fixtures;

namespace JAStudio.Core.Tests;

public abstract class TestStartingWithEmptyCollection : CollectionUsingTest
{
   protected TestStartingWithEmptyCollection() : base(DataNeeded.None) {}
}
