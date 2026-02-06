using System;
using System.Collections.Generic;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Note.Vocabulary;

/// <summary>
/// Tests ported from test_perfect_synonyms.py
/// </summary>
public class PerfectSynonymsTests : IDisposable
{
    private readonly IDisposable _collectionScope;

    public PerfectSynonymsTests() => _collectionScope = CollectionFactory.InjectEmptyCollection();

    public void Dispose()
    {
        _collectionScope.Dispose();
    }

    [Fact]
    public void AnswerSyncsToSynonymOnAdd()
    {
        var first = VocabNoteFactory.Create("first", "first_answer", []);
        var second = VocabNoteFactory.Create("second", "second_answer", []);

        first.RelatedNotes.PerfectSynonyms.AddOverwritingTheAnswerOfTheAddedSynonym(second.GetQuestion());
        Assert.Equal("first_answer", second.GetAnswer());
    }

    [Fact]
    public void AnswerSyncsToAddedSynonymOnUpdate()
    {
        var first = VocabNoteFactory.Create("first", "first_answer", []);
        var second = VocabNoteFactory.Create("second", "second_answer", []);

        first.RelatedNotes.PerfectSynonyms.AddOverwritingTheAnswerOfTheAddedSynonym(second.GetQuestion());

        first.User.Answer.Set("new answer");
        Assert.Equal("new answer", second.GetAnswer());

        var third = VocabNoteFactory.Create("third", "third_answer", []);
        third.RelatedNotes.PerfectSynonyms.AddOverwritingTheAnswerOfTheAddedSynonym(first.GetQuestion());
        Assert.Equal("third_answer", first.GetAnswer());
        Assert.Equal("third_answer", second.GetAnswer());

        third.User.Answer.Set("third_new");
        Assert.Equal("third_new", first.GetAnswer());
        Assert.Equal("third_new", second.GetAnswer());

        Assert.Equal([second.GetQuestion(), third.GetQuestion()], first.RelatedNotes.PerfectSynonyms.Get());
        Assert.Equal([first.GetQuestion(), third.GetQuestion()], second.RelatedNotes.PerfectSynonyms.Get());
        Assert.Equal([first.GetQuestion(), second.GetQuestion()], third.RelatedNotes.PerfectSynonyms.Get());

        first.RelatedNotes.PerfectSynonyms.Remove(third.GetQuestion());
        Assert.Equal([second.GetQuestion()], first.RelatedNotes.PerfectSynonyms.Get());
        Assert.Equal([first.GetQuestion()], second.RelatedNotes.PerfectSynonyms.Get());
        Assert.Empty(third.RelatedNotes.PerfectSynonyms.Get());

        first.User.Answer.Set("first_latest");
        Assert.Equal("first_latest", first.GetAnswer());
        Assert.Equal("first_latest", second.GetAnswer());
        Assert.Equal("third_new", third.GetAnswer());
    }

    [Fact]
    public void PerfectSynonymsAreKeptInSyncOnAdd()
    {
        var first = VocabNoteFactory.Create("first", "", []);
        var second = VocabNoteFactory.Create("second", "", []);
        first.RelatedNotes.PerfectSynonyms.AddOverwritingTheAnswerOfTheAddedSynonym(second.GetQuestion());

        Assert.Equal(["second"], first.RelatedNotes.PerfectSynonyms.Get());
        Assert.Equal(["first"], second.RelatedNotes.PerfectSynonyms.Get());

        var third = VocabNoteFactory.Create("third", "", []);
        var fourth = VocabNoteFactory.Create("fourth", "", []);
        second.RelatedNotes.PerfectSynonyms.AddOverwritingTheAnswerOfTheAddedSynonym(third.GetQuestion());
        second.RelatedNotes.PerfectSynonyms.AddOverwritingTheAnswerOfTheAddedSynonym(fourth.GetQuestion());

        Assert.Equal(["second", "third", "fourth"], first.RelatedNotes.PerfectSynonyms.Get());
        Assert.Equal(["first", "third", "fourth"], second.RelatedNotes.PerfectSynonyms.Get());
        Assert.Equal(["first", "second", "fourth"], third.RelatedNotes.PerfectSynonyms.Get());
        Assert.Equal(["first", "second", "third"], fourth.RelatedNotes.PerfectSynonyms.Get());
    }
}
