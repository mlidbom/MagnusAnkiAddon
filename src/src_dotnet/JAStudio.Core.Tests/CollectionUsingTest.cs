using System;
using System.Collections.Generic;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Note;
using JAStudio.Core.Tests.Fixtures;

namespace JAStudio.Core.Tests;

public abstract class CollectionUsingTest : IDisposable
{
   protected CollectionUsingTest(DataNeeded data = DataNeeded.All) =>
      _appScope = CollectionFactory.InjectCollectionWithSelectData(data);

   public void Dispose() => _appScope.Dispose();

   readonly CollectionFactory.AppScope _appScope;

   protected TService GetService<TService>() where TService : class => _appScope.App.Services.ServiceLocator.Resolve<TService>();

   protected NoteServices NoteServices => GetService<NoteServices>();

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
