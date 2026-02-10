using JAStudio.Core.Note;
using Xunit;

namespace JAStudio.Core.Tests.AICreatedTests.Note;

public class VocabNoteTests : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
   [Fact]
   public void VocabNote_Create_SetsBasicProperties()
   {
      // Arrange & Act
      var vocab = CreateVocab("食べる", "to eat", "たべる");

      // Assert
      Assert.NotNull(vocab);
      Assert.Equal("食べる", vocab.GetQuestion());
      Assert.Equal("to eat", vocab.GetAnswer());
      Assert.NotNull(vocab.GetId());
   }

   [Fact]
   public void VocabNote_GetReadings_ReturnsCorrectReadings()
   {
      // Arrange
      var vocab = CreateVocab("食べる", "to eat", "たべる", "くう");

      // Act
      var readings = vocab.GetReadings();

      // Assert
      Assert.Equal(2, readings.Count);
      Assert.Contains("たべる", readings);
      Assert.Contains("くう", readings);
   }

   [Fact]
   public void VocabNote_SetReadings_UpdatesReadings()
   {
      // Arrange
      var vocab = CreateVocab("本", "book", "ほん");

      // Act
      vocab.SetReadings(["ほん", "もと"]);
      var readings = vocab.GetReadings();

      // Assert
      Assert.Equal(2, readings.Count);
      Assert.Contains("ほん", readings);
      Assert.Contains("もと", readings);
   }

   [Fact]
   public void VocabNote_Question_HandlesDisambiguation()
   {
      // Arrange
      var vocab = new VocabNote(NoteServices);

      // Act
      vocab.Question.Set("取る:to take");

      // Assert
      Assert.True(vocab.Question.IsDisambiguated);
      Assert.Equal("取る", vocab.Question.Raw);
      Assert.Equal("取る:to take", vocab.Question.DisambiguationName);
   }

   [Fact]
   public void VocabNote_Question_RejectsInvalidDisambiguation()
   {
      // Arrange
      var vocab = new VocabNote(NoteServices);

      // Act
      vocab.Question.Set("a:b:c");

      // Assert
      Assert.False(vocab.Question.IsValid);
      Assert.Equal(JAStudio.Core.Note.Vocabulary.VocabNoteQuestion.InvalidQuestionMessage, vocab.Question.Raw);
   }

   [Fact]
   public void VocabNote_Forms_AddsAndRemovesForms()
   {
      // Arrange
      var vocab = CreateVocab("走る", "to run", "はしる");

      // Act - Add form
      vocab.Forms.Add("駆ける");
      var formsAfterAdd = vocab.Forms.AllList();

      // Assert - Form added
      Assert.Contains("駆ける", formsAfterAdd);

      // Act - Remove form
      vocab.Forms.Remove("駆ける");
      var formsAfterRemove = vocab.Forms.AllList();

      // Assert - Form removed
      Assert.DoesNotContain("駆ける", formsAfterRemove);
   }

   [Fact]
   public void VocabNote_Forms_IncludesQuestionAsOwnedForm()
   {
      // Arrange
      var vocab = CreateVocab("走る", "to run", "はしる");

      // Act
      var ownedForms = vocab.Forms.OwnedForms();

      // Assert
      Assert.Contains("走る", ownedForms);
   }

   [Fact]
   public void VocabNote_Forms_IdentifiesOwnedForms()
   {
      // Arrange
      var vocab = new VocabNote(NoteServices);
      vocab.Question.Set("走る");
      vocab.Forms.SetList(["[駆ける]", "はしる"]);

      // Act
      var isOwnedBracketed = vocab.Forms.IsOwnedForm("駆ける");
      var isOwnedQuestion = vocab.Forms.IsOwnedForm("走る");
      var isNotOwned = vocab.Forms.IsOwnedForm("はしる");

      // Assert
      Assert.True(isOwnedBracketed);
      Assert.True(isOwnedQuestion);
      Assert.False(isNotOwned);
   }

   [Fact]
   public void VocabNote_UserFields_StoresUserData()
   {
      // Arrange
      var vocab = CreateVocab("食べる", "to eat", "たべる");

      // Act
      vocab.User.Answer.Set("to consume");
      vocab.User.Mnemonic.Set("Remember 'taberu' sounds like 'table' where you eat");
      vocab.User.Explanation.Set("Common verb");

      // Assert
      Assert.Equal("to consume", vocab.User.Answer.Value);
      Assert.Equal("Remember 'taberu' sounds like 'table' where you eat", vocab.User.Mnemonic.Value);
      Assert.Equal("Common verb", vocab.User.Explanation.Value);
   }

   [Fact]
   public void VocabNote_GetAnswer_PreferesUserAnswer()
   {
      // Arrange
      var vocab = CreateVocab("本", "book", "ほん");

      // Act - Initially uses source answer
      var initialAnswer = vocab.GetAnswer();

      // Set user answer
      vocab.User.Answer.Set("written work");
      var userAnswer = vocab.GetAnswer();

      // Assert
      Assert.Equal("book", initialAnswer);
      Assert.Equal("written work", userAnswer);
   }

   [Fact]
   public void VocabNote_Question_AddsQuestionToFormsAutomatically()
   {
      // Arrange
      var vocab = new VocabNote(NoteServices);

      // Act
      vocab.Question.Set("新しい");

      // Assert
      Assert.Contains("新しい", vocab.Forms.AllSet());
   }

   [Fact]
   public void VocabNote_CreateWithForms_SetsForms()
   {
      // Arrange & Act
      var vocab = CreateVocab("食べる",
                              "to eat",
                              ["たべる"],
                              ["食う", "召し上がる"]);

      // Assert
      var forms = vocab.Forms.AllSet();
      Assert.Contains("食う", forms);
      Assert.Contains("召し上がる", forms);
   }
}
