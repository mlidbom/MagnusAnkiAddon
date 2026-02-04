using System;
using JAStudio.Core.Batches;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Batches;

/// <summary>
/// Tests ported from test_local_note_updater_smoke_tests_only.py
/// </summary>
public class LocalNoteUpdaterSmokeTests : IDisposable
{
    private readonly IDisposable _collectionScope;

    public LocalNoteUpdaterSmokeTests()
    {
        _collectionScope = CollectionFactory.InjectCollectionWithAllSampleData();
    }

    public void Dispose()
    {
        _collectionScope.Dispose();
    }

    [Fact]
    public void SmokeFullRebuild()
    {
        LocalNoteUpdater.FullRebuild();
    }
}
