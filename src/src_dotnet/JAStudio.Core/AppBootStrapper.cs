using Compze.Utilities.DependencyInjection;
using Compze.Utilities.DependencyInjection.Abstractions;
using Compze.Utilities.DependencyInjection.SimpleInjector;
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

static class AppBootstrapper
{
   public static App Bootstrap()
   {
      var container = new SimpleInjectorDependencyInjectionContainer();
      var registrar = container.Register();

      registrar.Register(
         Singleton.For<TemporaryServiceCollection>().CreatedBy(() => new TemporaryServiceCollection(container.ServiceLocator)),
         Singleton.For<App>().CreatedBy((TemporaryServiceCollection services) => new App(services)),
         Singleton.For<QueryBuilder>().CreatedBy((TemporaryServiceCollection services) => new QueryBuilder(services)),
         
         // Core services
         Singleton.For<ConfigurationValue>().CreatedBy((TemporaryServiceCollection services) => new ConfigurationValue(services)),
         Singleton.For<MyLog>().CreatedBy((TemporaryServiceCollection services) => new MyLog(services)),
         Singleton.For<ExPytest>().CreatedBy((TemporaryServiceCollection services) => new ExPytest(services)),
         Singleton.For<LocalNoteUpdater>().CreatedBy((TemporaryServiceCollection services) => new LocalNoteUpdater(services)),
         Singleton.For<TaskRunner>().CreatedBy((TemporaryServiceCollection services) => new TaskRunner(services)),
         Singleton.For<AnkiCardOperations>().CreatedBy((TemporaryServiceCollection services) => new AnkiCardOperations(services)),
         Singleton.For<DictLookup>().CreatedBy((TemporaryServiceCollection services) => new DictLookup(services)),
         Singleton.For<TestApp>().CreatedBy((TemporaryServiceCollection services) => new TestApp(services)),
         
         // Note services
         Singleton.For<KanjiNoteMnemonicMaker>().CreatedBy((TemporaryServiceCollection services) => new KanjiNoteMnemonicMaker(services)),
         Singleton.For<VocabNoteFactory>().CreatedBy((TemporaryServiceCollection services) => new VocabNoteFactory(services)),
         Singleton.For<VocabNoteSorting>().CreatedBy((TemporaryServiceCollection services) => new VocabNoteSorting(services)),
         Singleton.For<VocabNoteGeneratedData>().CreatedBy((TemporaryServiceCollection services) => new VocabNoteGeneratedData(services)),
         Singleton.For<VocabNoteMetaTagFormatter>().CreatedBy((TemporaryServiceCollection services) => new VocabNoteMetaTagFormatter(services)),
         Singleton.For<POSSetManager>().CreatedBy((TemporaryServiceCollection services) => new POSSetManager(services)),
         
         // ViewModels
         Singleton.For<SentenceKanjiListViewModel>().CreatedBy((TemporaryServiceCollection services) => new SentenceKanjiListViewModel(services)),
         
         // Renderers - Kanji
         Singleton.For<KanjiNoteRenderer>().CreatedBy((TemporaryServiceCollection services) => new KanjiNoteRenderer(services)),
         Singleton.For<DependenciesRenderer>().CreatedBy((TemporaryServiceCollection services) => new DependenciesRenderer(services)),
         Singleton.For<MnemonicRenderer>().CreatedBy((TemporaryServiceCollection services) => new MnemonicRenderer(services)),
         Singleton.For<ReadingsRenderer>().CreatedBy((TemporaryServiceCollection services) => new ReadingsRenderer(services)),
         Singleton.For<VocabListRenderer>().CreatedBy((TemporaryServiceCollection services) => new VocabListRenderer(services)),
         Singleton.For<KanjiListRenderer>().CreatedBy((TemporaryServiceCollection services) => new KanjiListRenderer(services)),
         
         // Renderers - Vocab
         Singleton.For<VocabNoteRenderer>().CreatedBy((TemporaryServiceCollection services) => new VocabNoteRenderer(services)),
         Singleton.For<VocabSentencesRenderer>().CreatedBy((TemporaryServiceCollection services) => new VocabSentencesRenderer(services)),
         Singleton.For<VocabKanjiListRenderer>().CreatedBy((TemporaryServiceCollection services) => new VocabKanjiListRenderer(services)),
         Singleton.For<RelatedVocabsRenderer>().CreatedBy((TemporaryServiceCollection services) => new RelatedVocabsRenderer(services)),
         Singleton.For<CompoundPartsRenderer>().CreatedBy((TemporaryServiceCollection services) => new CompoundPartsRenderer(services)),
         
         // Renderers - Sentence
         Singleton.For<SentenceNoteRenderer>().CreatedBy((TemporaryServiceCollection services) => new SentenceNoteRenderer(services)),
         Singleton.For<UdSentenceBreakdownRenderer>().CreatedBy((TemporaryServiceCollection services) => new UdSentenceBreakdownRenderer(services)),
         Singleton.For<QuestionRenderer>().CreatedBy((TemporaryServiceCollection services) => new QuestionRenderer(services)),
         Singleton.For<SentenceRenderer>().CreatedBy((TemporaryServiceCollection services) => new SentenceRenderer(services)),
         
         // Web
         Singleton.For<DisplayType>().CreatedBy((TemporaryServiceCollection services) => new DisplayType(services))
      );

      return container.ServiceLocator.Resolve<App>();
   }
}