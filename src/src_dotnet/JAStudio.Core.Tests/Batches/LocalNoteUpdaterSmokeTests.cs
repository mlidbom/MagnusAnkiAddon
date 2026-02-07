using System;
using JAStudio.Core.Batches;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Batches;

/// <summary>
/// Tests ported from test_local_note_updater_smoke_tests_only.py
/// </summary>
public class LocalNoteUpdaterSmokeTests : CollectionUsingTest
{
    [Fact]
    public void SmokeFullRebuild()
    {
        GetService<LocalNoteUpdater>().FullRebuild();
    }
}
