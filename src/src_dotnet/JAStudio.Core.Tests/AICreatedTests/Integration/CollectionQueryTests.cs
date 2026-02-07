using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.TestUtils;
using Xunit;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.Tests.AICreatedTests.Integration;

public class CollectionQueryTests : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
    [Fact]
    public void VocabCollection_WithQuestion_FindsVocabByQuestion()
    {
        // Arrange
        var vocab1 = VocabNote.Create("食べる", "to eat", "たべる");
        var vocab2 = VocabNote.Create("本", "book", "ほん");
        var vocab3 = VocabNote.Create("走る", "to run", "はしる");

        // Act
        var results = GetService<VocabCollection>().WithQuestion("\u672c");

        // Assert
        Assert.Single(results);
        Assert.Equal(vocab2, results.First());
    }

    [Fact]
    public void VocabCollection_WithQuestion_DoesNotFindByForm()
    {
        // Arrange
        var vocab = VocabNote.Create("食べる", "to eat", "たべる");
        vocab.Forms.Add("食う");

        // Act - Forms are not questions, so this should not find the vocab
        var results = GetService<VocabCollection>().WithQuestion("食う");

        // Assert - Should be empty because "食う" is a form, not the question
        Assert.Empty(results);
    }

    [Fact]
    public void VocabCollection_WithQuestion_ReturnsEmptyWhenNotFound()
    {
        // Arrange
        var vocab = VocabNote.Create("食べる", "to eat", "たべる");

        // Act
        var results = GetService<VocabCollection>().WithQuestion("存在しない");

        // Assert
        Assert.Empty(results);
    }

    [Fact]
    public void KanjiCollection_WithKanji_FindsKanjiByQuestion()
    {
        // Arrange
        var kanji1 = KanjiNote.Create("食", "eat", "ショク", "た");
        var kanji2 = KanjiNote.Create("本", "book", "ホン", "もと");

        // Act
        var result = GetService<KanjiCollection>().WithKanji("食");

        // Assert
        Assert.NotNull(result);
        Assert.Equal(kanji1, result);
    }

    [Fact]
    public void KanjiCollection_WithKanji_ReturnsNullWhenNotFound()
    {
        // Arrange
        var kanji = KanjiNote.Create("食", "eat", "ショク", "た");

        // Act
        var result = GetService<KanjiCollection>().WithKanji("存");

        // Assert
        Assert.Null(result);
    }

    [Fact]
    public void SentenceCollection_Add_MakesNoteQueryable()
    {
        // Arrange
        var sentence = SentenceNote.CreateTestNote("これは本です。", "This is a book.");

        // Act - Note is automatically added in CreateTestNote
        var allSentences = GetService<SentenceCollection>().All();

        // Assert
        Assert.Contains(sentence, allSentences);
    }

    [Fact]
    public void MultipleCollections_IndependentlyManageNotes()
    {
        // Arrange
        var kanji = KanjiNote.Create("食", "eat", "ショク", "た");
        var vocab = VocabNote.Create("食べる", "to eat", "たべる");
        var sentence = SentenceNote.CreateTestNote("食べる", "to eat");

        // Act
        var kanjiCount = GetService<KanjiCollection>().All().Count;
        var vocabCount = GetService<VocabCollection>().All().Count;
        var sentenceCount = GetService<SentenceCollection>().All().Count;

        // Assert
        Assert.Equal(1, kanjiCount);
        Assert.Equal(1, vocabCount);
        Assert.Equal(1, sentenceCount);
    }

    [Fact]
    public void VocabCollection_ById_ReturnsCorrectNote()
    {
        // Arrange
        var vocab1 = VocabNote.Create("食べる", "to eat", "たべる");
        var vocab2 = VocabNote.Create("本", "book", "ほん");
        var id1 = vocab1.GetId();

        // Act
        var result = GetService<VocabCollection>().WithIdOrNone(id1);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(vocab1, result);
        Assert.NotEqual(vocab2, result);
    }
}
