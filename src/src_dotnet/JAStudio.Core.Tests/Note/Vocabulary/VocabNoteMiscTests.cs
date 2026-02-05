using System;
using System.Text.RegularExpressions;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Note.Vocabulary;

/// <summary>
/// Tests ported from test_vocabnote_misc.py
/// </summary>
public class VocabNoteMiscTests : IDisposable
{
    private readonly IDisposable _collectionScope;

    public VocabNoteMiscTests()
    {
        _collectionScope = CollectionFactory.InjectEmptyCollection();
    }

    public void Dispose()
    {
        _collectionScope.Dispose();
    }

    [Fact]
    public void FormsExclusionRegex()
    {
        var formsExclusions = new Regex(@"\[\[.*]]");
        Assert.Matches(formsExclusions, "[[らっしゃる]]");
    }

    [Fact]
    public void GenerateFromDictionary()
    {
        var vocab = VocabNoteFactory.CreateWithDictionary("やる気満々");
        Assert.Equal("やる気満々", vocab.GetQuestion());
        Assert.Equal("totally-willing/fully-motivated", vocab.GetAnswer());
        Assert.Equal(["やるきまんまん"], vocab.Readings.Get());
    }
}
