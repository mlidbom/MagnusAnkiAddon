using JAStudio.Core.Note;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.AICreatedTests.Note;

public class KanjiNoteTests : IAIGeneratedTestClass
{
    public KanjiNoteTests()
    {
        TestApp.Initialize();
    }

    [Fact]
    public void KanjiNote_Create_SetsBasicProperties()
    {
        // Arrange & Act
        var kanji = KanjiNote.Create("漢", "Chinese character", "カン、かん", "");

        // Assert
        Assert.NotNull(kanji);
        Assert.Equal("漢", kanji.GetQuestion());
        Assert.Equal("Chinese character", kanji.GetAnswer());
        Assert.NotEqual(0, kanji.GetId());
    }

    [Fact]
    public void KanjiNote_GetReadingsOn_ReturnsCorrectReadings()
    {
        // Arrange
        var kanji = KanjiNote.Create("漢", "Chinese character", "カン、かん", "");

        // Act
        var readings = kanji.GetReadingsOn();

        // Assert
        Assert.Contains("カン", readings);
        Assert.Contains("かん", readings);
    }

    [Fact]
    public void KanjiNote_GetRadicals_ExcludesOwnKanji()
    {
        // Arrange
        var kanji = new KanjiNote();
        kanji.SetQuestion("漢");
        kanji.SetField(NoteFieldsConstants.Kanji.Radicals, "漢, 水, 口");

        // Act
        var radicals = kanji.GetRadicals();

        // Assert
        Assert.DoesNotContain("漢", radicals);
        Assert.Contains("水", radicals);
        Assert.Contains("口", radicals);
    }

    [Fact]
    public void KanjiNote_GetPrimaryReadings_ExtractsMarkedReadings()
    {
        // Arrange
        var kanji = new KanjiNote();
        kanji.SetReadingOn("<primary>カン</primary>, ケン");

        // Act
        var primaryReadings = kanji.GetPrimaryReadingsOn();

        // Assert
        Assert.Single(primaryReadings);
        Assert.Equal("カン", primaryReadings[0]);
    }

    [Fact]
    public void KanjiNote_AddPrimaryReading_MarksReading()
    {
        // Arrange
        var kanji = new KanjiNote();
        kanji.SetReadingOn("カン, ケン");

        // Act
        kanji.AddPrimaryOnReading("カン");

        // Assert
        Assert.Contains("<primary>カン</primary>", kanji.GetReadingOnHtml());
    }

    [Fact]
    public void KanjiNote_RemovePrimaryReading_UnmarksReading()
    {
        // Arrange
        var kanji = new KanjiNote();
        kanji.SetReadingOn("<primary>カン</primary>, ケン");

        // Act
        kanji.RemovePrimaryOnReading("カン");

        // Assert
        Assert.DoesNotContain("<primary>カン</primary>", kanji.GetReadingOnHtml());
        Assert.Contains("カン", kanji.GetReadingOnHtml());
    }
}
