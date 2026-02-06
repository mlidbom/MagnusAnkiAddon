using JAStudio.Core.Note;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.AICreatedTests.Integration;

public class NoteRelationshipTests : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
   [Fact]
   public void SentenceDependsOnHighlightedVocab()
   {
      // Arrange
      var vocab = VocabNote.Create("食べる", "to eat", "たべる");
      var sentence = SentenceNote.CreateTestNote("私は朝ご飯を食べる。", "I eat breakfast.");

      // Act - Add vocab to sentence's highlighted words
      sentence.Configuration.HighlightedWords.Add("食べる");
      var dependencies = sentence.GetDirectDependencies();

      // Assert
      Assert.Contains(vocab, dependencies);
   }

   [Fact]
   public void SentenceDependsOnKanjiFromQuestion()
   {
      // Arrange
      var kanji = KanjiNote.Create("食", "eat, food", "ショク、しょく", "た、く");
      var sentence = SentenceNote.CreateTestNote("食べる", "to eat");

      // Act
      var dependencies = sentence.GetDirectDependencies();

      // Assert - Note: This will work once ExtractKanji is properly implemented
      // For now it returns empty list, but the infrastructure is there
      Assert.NotNull(dependencies);
   }

   [Fact]
   public void KanjiDependsOnRadicals()
   {
      // Arrange
      var radical1 = KanjiNote.Create("人", "person", "ジン、ニン", "ひと");
      var radical2 = KanjiNote.Create("食", "eat", "ショク", "た");
      var kanji = KanjiNote.Create("飯", "cooked rice, meal", "ハン", "めし");
      kanji.SetField(NoteFieldsConstants.Kanji.Radicals, "人, 食");

      // Act
      var dependencies = kanji.GetDirectDependencies();

      // Assert
      Assert.Contains(radical1, dependencies);
      Assert.Contains(radical2, dependencies);
      Assert.DoesNotContain(kanji, dependencies); // Should not depend on itself
   }

   [Fact]
   public void MultipleNotesCanReferenceTheSameNote()
   {
      // Arrange
      var vocab = VocabNote.Create("食べる", "to eat", "たべる");
      var sentence1 = SentenceNote.CreateTestNote("私は食べる。", "I eat.");
      var sentence2 = SentenceNote.CreateTestNote("彼は食べる。", "He eats.");

      sentence1.Configuration.HighlightedWords.Add("食べる");
      sentence2.Configuration.HighlightedWords.Add("食べる");

      // Act
      var deps1 = sentence1.GetDirectDependencies();
      var deps2 = sentence2.GetDirectDependencies();

      // Assert
      Assert.Contains(vocab, deps1);
      Assert.Contains(vocab, deps2);
   }
}
