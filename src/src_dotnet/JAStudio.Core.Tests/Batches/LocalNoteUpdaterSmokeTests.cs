using JAStudio.Core.Batches;
using Xunit;

namespace JAStudio.Core.Tests.Batches;

/// <summary>
/// Tests ported from test_local_note_updater_smoke_tests_only.py
/// </summary>
public class LocalNoteUpdaterSmokeTests : SpecificationUsingACollection
{
   [Fact]
   public void SmokeFullRebuild()
   {
      GetService<LocalNoteUpdater>().FullRebuild();
   }
}
