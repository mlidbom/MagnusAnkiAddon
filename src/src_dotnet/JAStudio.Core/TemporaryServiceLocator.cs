using System;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Anki;
using JAStudio.Core.AnkiUtils;
using JAStudio.Core.Batches;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.TestUtils;
using JAStudio.Core.UI.Web.Kanji;
using JAStudio.Core.UI.Web.Sentence;
using JAStudio.Core.UI.Web.Vocab;
using JAStudio.Core.ViewModels.KanjiList;

namespace JAStudio.Core;

//TODO: We should redesign so that we have a sane dependency graph and just use normal dependency injection, but first we need to get rid of all the static classes and this will help us do that
public class TemporaryServiceCollection(IServiceLocator serviceLocator) : IDisposable
{
   readonly IServiceLocator _serviceLocator = serviceLocator;

   public App App => _serviceLocator.Resolve<App>();
   public QueryBuilder QueryBuilder => _serviceLocator.Resolve<QueryBuilder>();

   // Core services
   public LocalNoteUpdater LocalNoteUpdater => _serviceLocator.Resolve<LocalNoteUpdater>();
   public TaskRunner TaskRunner => _serviceLocator.Resolve<TaskRunner>();
   public AnkiCardOperations AnkiCardOperations => _serviceLocator.Resolve<AnkiCardOperations>();
   public DictLookup DictLookup => _serviceLocator.Resolve<DictLookup>();
   public TestApp TestApp => _serviceLocator.Resolve<TestApp>();

   // Note services
   public KanjiNoteMnemonicMaker KanjiNoteMnemonicMaker => _serviceLocator.Resolve<KanjiNoteMnemonicMaker>();
   public VocabNoteFactory VocabNoteFactory => _serviceLocator.Resolve<VocabNoteFactory>();
   public VocabNoteGeneratedData VocabNoteGeneratedData => _serviceLocator.Resolve<VocabNoteGeneratedData>();

   // ViewModels
   public SentenceKanjiListViewModel SentenceKanjiListViewModel => _serviceLocator.Resolve<SentenceKanjiListViewModel>();

   // Renderers
   public KanjiListRenderer KanjiListRenderer => _serviceLocator.Resolve<KanjiListRenderer>();
   public VocabKanjiListRenderer VocabKanjiListRenderer => _serviceLocator.Resolve<VocabKanjiListRenderer>();
   public RelatedVocabsRenderer RelatedVocabsRenderer => _serviceLocator.Resolve<RelatedVocabsRenderer>();
   public UdSentenceBreakdownRenderer UdSentenceBreakdownRenderer => _serviceLocator.Resolve<UdSentenceBreakdownRenderer>();
   public QuestionRenderer QuestionRenderer => _serviceLocator.Resolve<QuestionRenderer>();
   public SentenceRenderer SentenceRenderer => _serviceLocator.Resolve<SentenceRenderer>();

   public void Dispose() => _serviceLocator.Dispose();
}
