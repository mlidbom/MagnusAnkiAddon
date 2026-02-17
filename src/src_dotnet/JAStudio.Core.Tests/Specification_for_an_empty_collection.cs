using JAStudio.Core.Tests.Fixtures;

namespace JAStudio.Core.Tests;

public abstract class Specification_for_an_empty_collection : Specification_using_a_collection
{
   protected Specification_for_an_empty_collection() : base(DataNeeded.None) {}
}
