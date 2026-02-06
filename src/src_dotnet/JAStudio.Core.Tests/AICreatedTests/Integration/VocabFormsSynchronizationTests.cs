using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.AICreatedTests.Integration;

public class VocabFormsSynchronizationTests : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
   [Fact]
   public void AddingFormToVocabA_UpdatesVocabB_WhenVocabBHasThatFormAsQuestion()
   {
      // Arrange
      var vocabA = VocabNote.Create("食べる", "to eat", "たべる");
      var vocabB = VocabNote.Create("食う", "to eat (casual)", "くう");

      // Act - Add vocabB's question as a form of vocabA
      vocabA.Forms.Add("食う");

      // Assert - VocabB should now have vocabA's question as a form
      Assert.Contains("食べる", vocabB.Forms.AllSet());
   }

   [Fact]
   public void RemovingFormFromVocabA_UpdatesVocabB()
   {
      // Arrange
      var vocabA = VocabNote.Create("走る", "to run", "はしる");
      var vocabB = VocabNote.Create("駆ける", "to run, to dash", "かける");

      vocabA.Forms.Add("駆ける");
      Assert.Contains("走る", vocabB.Forms.AllSet()); // Verify it was added

      // Act - Remove the form
      vocabA.Forms.Remove("駆ける");

      // Assert - VocabB should no longer have vocabA's question as a form
      Assert.DoesNotContain("走る", vocabB.Forms.AllSet());
   }

   [Fact]
   public void OwnedForms_IdentifiedByBrackets()
   {
      // Arrange
      var vocab = VocabNote.Create("走る", "to run", "はしる");

      // Act - Set forms with bracketed (owned) and non-bracketed (borrowed) forms
      vocab.Forms.SetList(["[駆ける]", "ダッシュする"]);

      // Assert
      Assert.True(vocab.Forms.IsOwnedForm("駆ける"));
      Assert.True(vocab.Forms.IsOwnedForm("走る")); // Question is always owned
      Assert.False(vocab.Forms.IsOwnedForm("ダッシュする"));
   }

   [Fact]
   public void QuestionAlwaysIncludedInOwnedForms()
   {
      // Arrange & Act
      var vocab = VocabNote.Create("本", "book", "ほん");

      // Assert
      var ownedForms = vocab.Forms.OwnedForms();
      Assert.Contains("本", ownedForms);
   }

   [Fact]
   public void AllListNotes_ReturnsNotesForAllForms()
   {
      // Arrange
      var vocab1 = VocabNote.Create("食べる", "to eat", "たべる");
      var vocab2 = VocabNote.Create("食う", "to eat (casual)", "くう");
      var vocab3 = VocabNote.Create("召し上がる", "to eat (honorific)", "めしあがる");

      vocab1.Forms.SetList(["食う", "召し上がる"]);

      // Act
      var formNotes = vocab1.Forms.AllListNotes();

      // Assert
      Assert.Contains(vocab2, formNotes);
      Assert.Contains(vocab3, formNotes);
   }
}
