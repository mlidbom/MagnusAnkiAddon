using System;
using System.Text.RegularExpressions;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Note.Vocabulary;

/// <summary>
/// Tests ported from test_vocabnote_misc.py
/// </summary>
public class VocabNoteMiscTests : TestStartingWithEmptyCollection
{
    [Fact]
    public void FormsExclusionRegex()
    {
        var formsExclusions = new Regex(@"\[\[.*]]");
        Assert.Matches(formsExclusions, "[[らっしゃる]]");
    }

    [Fact]
    public void GenerateFromDictionary()
    {
        var vocab = TemporaryServiceCollection.Instance.VocabNoteFactory.CreateWithDictionary("やる気満々");
        Assert.Equal("やる気満々", vocab.GetQuestion());
        Assert.Equal("totally-willing/fully-motivated", vocab.GetAnswer());
        Assert.Equal(["やるきまんまん"], vocab.Readings.Get());
    }
}
