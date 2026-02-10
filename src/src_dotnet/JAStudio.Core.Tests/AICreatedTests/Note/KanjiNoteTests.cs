using JAStudio.Core.Note;
using Xunit;

namespace JAStudio.Core.Tests.AICreatedTests.Note;

public class KanjiNoteTests : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
   [Fact]
   public void KanjiNote_Create_SetsBasicProperties()
   {
      // Arrange & Act
      var kanji = CreateKanji("漢", "Chinese character", "カン、かん", "");

      // Assert
      Assert.NotNull(kanji);
      Assert.Equal("漢", kanji.GetQuestion());
      Assert.Equal("Chinese character", kanji.GetAnswer());
      Assert.NotNull(kanji.GetId());
   }

   [Fact]
   public void KanjiNote_GetReadingsOn_ReturnsCorrectReadings()
   {
      // Arrange
      var kanji = CreateKanji("漢", "Chinese character", "カン、かん", "");

      // Act
      var readings = kanji.ReadingsOn;

      // Assert
      Assert.Contains("カン", readings);
      Assert.Contains("かん", readings);
   }

   [Fact]
   public void KanjiNote_GetRadicals_ExcludesOwnKanji()
   {
      // Arrange
      var kanji = new KanjiNote(NoteServices);
      kanji.SetQuestion("漢");
      kanji.SetField(NoteFieldsConstants.Kanji.Radicals, "漢, 水, 口");

      // Act
      var radicals = kanji.Radicals;

      // Assert
      Assert.DoesNotContain("漢", radicals);
      Assert.Contains("水", radicals);
      Assert.Contains("口", radicals);
   }

   [Fact]
   public void KanjiNote_GetPrimaryReadings_ExtractsMarkedReadings()
   {
      // Arrange
      var kanji = new KanjiNote(NoteServices);
      kanji.ReadingOnHtml = "<primary>カン</primary>, ケン";

      // Act
      var primaryReadings = kanji.PrimaryReadingsOn;

      // Assert
      Assert.Single(primaryReadings);
      Assert.Equal("カン", primaryReadings[0]);
   }

   [Fact]
   public void KanjiNote_AddPrimaryReading_MarksReading()
   {
      // Arrange
      var kanji = new KanjiNote(NoteServices);
      kanji.ReadingOnHtml = "カン, ケン";

      // Act
      kanji.AddPrimaryOnReading("カン");

      // Assert
      Assert.Contains("<primary>カン</primary>", kanji.ReadingOnHtml);
   }

   [Fact]
   public void KanjiNote_RemovePrimaryReading_UnmarksReading()
   {
      // Arrange
      var kanji = new KanjiNote(NoteServices);
      kanji.ReadingOnHtml = "<primary>カン</primary>, ケン";

      // Act
      kanji.RemovePrimaryOnReading("カン");

      // Assert
      Assert.DoesNotContain("<primary>カン</primary>", kanji.ReadingOnHtml);
      Assert.Contains("カン", kanji.ReadingOnHtml);
   }
}
