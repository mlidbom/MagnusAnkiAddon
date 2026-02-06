using JAStudio.Core.Note;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.AICreatedTests.Integration;

public class CacheInvalidationTests : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
    [Fact]
    public void UpdatingVocabQuestion_UpdatesCache()
    {
        // Arrange
        var vocab = VocabNote.Create("食べる", "to eat", "たべる");
        var originalQuestion = vocab.GetQuestion();

        // Act
        vocab.Question.Set("飲む");
        vocab.UpdateGeneratedData(); // Trigger cache update

        // Assert - Old question should not find it
        var oldResults = App.Col().Vocab.WithQuestion("食べる");
        Assert.Empty(oldResults);

        // New question should find it
        var newResults = App.Col().Vocab.WithQuestion("飲む");
        Assert.Single(newResults);
        Assert.Equal(vocab, newResults[0]);
    }

    [Fact]
    public void AddingVocabForm_DoesNotMakeItFindableByWithQuestion()
    {
        // Arrange
        var vocab = VocabNote.Create("食べる", "to eat", "たべる");

        // Act - Add a form that doesn't exist as another vocab's question
        vocab.Forms.Add("taberu-form");

        // Assert - Forms are not questions, so WithQuestion should NOT find it
        var results = App.Col().Vocab.WithQuestion("taberu-form");
        Assert.Empty(results);

        // But it should still be findable by its actual question
        var byQuestion = App.Col().Vocab.WithQuestion("\u98df\u3079\u308b");
        Assert.Single(byQuestion);
    }

    [Fact]
    public void RemovingVocabForm_StillFindableByQuestion()
    {
        // Arrange
        var vocab = VocabNote.Create("食べる", "to eat", "たべる");
        vocab.Forms.Add("食う");

        // Verify forms are stored
        Assert.Contains("食う", vocab.Forms.AllSet());

        // Act - Remove the form
        vocab.Forms.Remove("食う");

        // Assert - Form should be removed
        Assert.DoesNotContain("食う", vocab.Forms.AllSet());

        // But still findable by its question
        var results = App.Col().Vocab.WithQuestion("食べる");
        Assert.Single(results);
    }

    [Fact]
    public void UpdatingKanjiQuestion_UpdatesCache()
    {
        // Arrange
        var kanji = KanjiNote.Create("食", "eat", "ショク", "た");

        // Act
        kanji.SetQuestion("飲");
        kanji.UpdateGeneratedData();

        // Assert
        Assert.Null(App.Col().Kanji.WithKanji("食"));
        Assert.NotNull(App.Col().Kanji.WithKanji("飲"));
        Assert.Equal(kanji, App.Col().Kanji.WithKanji("飲"));
    }

    [Fact]
    public void MultipleUpdates_MaintainCacheConsistency()
    {
        // Arrange
        var vocab = VocabNote.Create("走る", "to run", "はしる");

        // Act - Multiple updates
        vocab.Forms.Add("駆ける");
        vocab.Forms.Add("ダッシュする");
        vocab.Question.Set("疾走する");
        vocab.UpdateGeneratedData();
        vocab.Forms.Remove("駆ける");

        // Assert - Cache should reflect final state
        var byNewQuestion = App.Col().Vocab.WithQuestion("疾走する");
        Assert.Single(byNewQuestion);

        // Old question should not find it
        var byOldQuestion = App.Col().Vocab.WithQuestion("走る");
        Assert.Empty(byOldQuestion);

        // Forms should be stored correctly
        Assert.DoesNotContain("駆ける", vocab.Forms.AllSet());
        Assert.Contains("ダッシュする", vocab.Forms.AllSet());
    }
}
