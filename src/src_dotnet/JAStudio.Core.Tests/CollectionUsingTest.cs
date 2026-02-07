using System;
using System.Collections.Generic;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Note;
using JAStudio.Core.Tests.Fixtures;

namespace JAStudio.Core.Tests;

public abstract class CollectionUsingTest : IDisposable
{
   protected CollectionUsingTest(DataNeeded data = DataNeeded.All) =>
      _collectionScope = CollectionFactory.InjectCollectionWithSelectData(data);

   public void Dispose() => _collectionScope.Dispose();

   readonly IDisposable _collectionScope;

   protected TService GetService<TService>() where TService : class => TemporaryServiceCollection.Instance.ServiceLocator.Resolve<TService>();

   protected NoteServices NoteServices => TemporaryServiceCollection.Instance.NoteServices;

   protected VocabNote CreateVocab(string question, string answer, params string[] readings) =>
      VocabNote.Create(NoteServices, question, answer, readings);

   protected VocabNote CreateVocab(string question, string answer, List<string> readings, List<string> forms) =>
      VocabNote.Create(NoteServices, question, answer, readings, forms);

   protected KanjiNote CreateKanji(string question, string answer, string onReadings, string kunReading) =>
      KanjiNote.Create(NoteServices, question, answer, onReadings, kunReading);

   protected SentenceNote CreateSentence(string question) =>
      SentenceNote.Create(NoteServices, question);

   protected SentenceNote CreateTestSentence(string question, string answer) =>
      SentenceNote.CreateTestNote(NoteServices, question, answer);
}
