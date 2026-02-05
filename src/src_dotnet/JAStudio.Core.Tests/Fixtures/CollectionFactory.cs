using System;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Tests.Fixtures.BaseData.SampleData;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core.Tests.Fixtures;

public static class CollectionFactory
{
    public static IDisposable InjectEmptyCollection()
    {
        TestApp.Reset();
        return new CollectionScope();
    }

    public static IDisposable InjectCollectionWithSelectData(bool kanji = false, bool specialVocab = false, bool sentences = false)
    {
        TestApp.Reset();
        
        if (kanji)
        {
            foreach (var kanjiSpec in KanjiSpec.TestKanjiList)
            {
                KanjiNote.Create(kanjiSpec.Question, kanjiSpec.Answer, kanjiSpec.OnReadings, kanjiSpec.KunReading);
            }
        }

        if (specialVocab)
        {
            foreach (var vocab in VocabLists.TestSpecialVocab)
            {
                vocab.CreateVocabNote();
            }
        }

        if (sentences)
        {
            foreach (var sentence in SentenceSpec.TestSentenceList)
            {
                SentenceNote.CreateTestNote(sentence.Question, sentence.Answer);
            }
        }

        return new CollectionScope();
    }

    public static IDisposable InjectCollectionWithAllSampleData()
    {
        return InjectCollectionWithSelectData(kanji: true, specialVocab: true, sentences: true);
    }

    private class CollectionScope : IDisposable
    {
        public void Dispose()
        {
            // No cleanup needed - next test will call Reset()
        }
    }
}
