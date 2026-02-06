using Xunit;

namespace JAStudio.Core.Tests;

public class BootStrappingTests
{
   [Fact]
   public void BootstrappingSmokeTest()
   {
      using var _ = App.Bootstrap();
   }
}
