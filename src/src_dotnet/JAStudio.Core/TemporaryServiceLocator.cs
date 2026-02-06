using System;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Anki;
using JAStudio.Core.AnkiUtils;
using JAStudio.Core.Batches;
using JAStudio.Core.Configuration;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.TestUtils;
using JAStudio.Core.UI.Web;
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
   public ConfigurationValue ConfigurationValue => _serviceLocator.Resolve<ConfigurationValue>();
   public MyLog MyLog => _serviceLocator.Resolve<MyLog>();
   public ExPytest ExPytest => _serviceLocator.Resolve<ExPytest>();
   public LocalNoteUpdater LocalNoteUpdater => _serviceLocator.Resolve<LocalNoteUpdater>();
   public TaskRunner TaskRunner => _serviceLocator.Resolve<TaskRunner>();
   public AnkiCardOperations AnkiCardOperations => _serviceLocator.Resolve<AnkiCardOperations>();
   public DictLookup DictLookup => _serviceLocator.Resolve<DictLookup>();
   public TestApp TestApp => _serviceLocator.Resolve<TestApp>();
   
   // Note services
   public KanjiNoteMnemonicMaker KanjiNoteMnemonicMaker => _serviceLocator.Resolve<KanjiNoteMnemonicMaker>();
   public VocabNoteFactory VocabNoteFactory => _serviceLocator.Resolve<VocabNoteFactory>();
   public VocabNoteSorting VocabNoteSorting => _serviceLocator.Resolve<VocabNoteSorting>();
   public VocabNoteGeneratedData VocabNoteGeneratedData => _serviceLocator.Resolve<VocabNoteGeneratedData>();
   public VocabNoteMetaTagFormatter VocabNoteMetaTagFormatter => _serviceLocator.Resolve<VocabNoteMetaTagFormatter>();
   public POSSetManager POSSetManager => _serviceLocator.Resolve<POSSetManager>();
   
   // ViewModels
   public SentenceKanjiListViewModel SentenceKanjiListViewModel => _serviceLocator.Resolve<SentenceKanjiListViewModel>();
   
   // Renderers - Kanji
   public KanjiNoteRenderer KanjiNoteRenderer => _serviceLocator.Resolve<KanjiNoteRenderer>();
   public DependenciesRenderer DependenciesRenderer => _serviceLocator.Resolve<DependenciesRenderer>();
   public MnemonicRenderer MnemonicRenderer => _serviceLocator.Resolve<MnemonicRenderer>();
   public ReadingsRenderer ReadingsRenderer => _serviceLocator.Resolve<ReadingsRenderer>();
   public VocabListRenderer VocabListRenderer => _serviceLocator.Resolve<VocabListRenderer>();
   public KanjiListRenderer KanjiListRenderer => _serviceLocator.Resolve<KanjiListRenderer>();
   
   // Renderers - Vocab
   public VocabNoteRenderer VocabNoteRenderer => _serviceLocator.Resolve<VocabNoteRenderer>();
   public VocabSentencesRenderer VocabSentencesRenderer => _serviceLocator.Resolve<VocabSentencesRenderer>();
   public VocabKanjiListRenderer VocabKanjiListRenderer => _serviceLocator.Resolve<VocabKanjiListRenderer>();
   public RelatedVocabsRenderer RelatedVocabsRenderer => _serviceLocator.Resolve<RelatedVocabsRenderer>();
   public CompoundPartsRenderer CompoundPartsRenderer => _serviceLocator.Resolve<CompoundPartsRenderer>();
   
   // Renderers - Sentence
   public SentenceNoteRenderer SentenceNoteRenderer => _serviceLocator.Resolve<SentenceNoteRenderer>();
   public UdSentenceBreakdownRenderer UdSentenceBreakdownRenderer => _serviceLocator.Resolve<UdSentenceBreakdownRenderer>();
   public QuestionRenderer QuestionRenderer => _serviceLocator.Resolve<QuestionRenderer>();
   public SentenceRenderer SentenceRenderer => _serviceLocator.Resolve<SentenceRenderer>();
   
   // Web
   public DisplayType DisplayType => _serviceLocator.Resolve<DisplayType>();

   public void Dispose() => _serviceLocator.Dispose();
}
