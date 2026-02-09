using Compze.Utilities.DependencyInjection;
using Compze.Utilities.DependencyInjection.Abstractions;
using Compze.Utilities.DependencyInjection.SimpleInjector;
using JAStudio.Core.Anki;
using JAStudio.Core.AnkiUtils;
using JAStudio.Core.Configuration;
using JAStudio.Core.Batches;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.LanguageServices.JanomeEx;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.TestUtils;
using JAStudio.Core.UI.Web.Kanji;
using JAStudio.Core.UI.Web.Sentence;
using JAStudio.Core.UI.Web.Vocab;
using JAStudio.Core.ViewModels.KanjiList;

namespace JAStudio.Core;

static class AppBootstrapper
{
   internal static IServiceLocator Bootstrap(App app)
   {
      IBackendNoteCreator backendNoteCreator = TestEnvDetector.IsTesting ? new TestingBackendNoteCreator() : new AnkiBackendNoteCreator();

      var container = new SimpleInjectorDependencyInjectionContainer();
      var registrar = container.Register();

      registrar.Register(
         Singleton.For<IBackendNoteCreator>().Instance(backendNoteCreator),
         Singleton.For<App>().Instance(app),
         Singleton.For<ConfigurationStore>().CreatedBy((TemporaryServiceCollection services) => new ConfigurationStore(services)),
         Singleton.For<TemporaryServiceCollection>().CreatedBy(() => new TemporaryServiceCollection(container.ServiceLocator)),
         Singleton.For<JapaneseConfig>().CreatedBy((ConfigurationStore store) => store.Config()),
         Singleton.For<JPCollection>().CreatedBy((AnkiCardOperations ankiCardOps, Settings settings, KanjiNoteMnemonicMaker kanjiMnemonicMaker, JapaneseConfig config, TaskRunner taskRunner) =>
                                                    new JPCollection(backendNoteCreator, ankiCardOps, settings, kanjiMnemonicMaker, config, taskRunner)),
         Singleton.For<VocabCollection>().CreatedBy((JPCollection col) => col.Vocab),
         Singleton.For<KanjiCollection>().CreatedBy((JPCollection col) => col.Kanji),
         Singleton.For<SentenceCollection>().CreatedBy((JPCollection col) => col.Sentences),

         // Core services
         Singleton.For<Settings>().CreatedBy((JapaneseConfig config) => new Settings(config)),
         Singleton.For<AnalysisServices>().CreatedBy((VocabCollection vocab, DictLookup dictLookup, Settings settings) => new AnalysisServices(vocab, dictLookup, settings)),
         Singleton.For<AnkiNoteIdMap>().CreatedBy(() => new AnkiNoteIdMap()),
         Singleton.For<QueryBuilder>().CreatedBy((VocabCollection vocab, KanjiCollection kanji, AnalysisServices analysisServices, AnkiNoteIdMap ankiNoteIdMap) => new QueryBuilder(vocab, kanji, analysisServices, ankiNoteIdMap)),
         Singleton.For<LocalNoteUpdater>().CreatedBy((TaskRunner taskRunner, VocabCollection vocab, KanjiCollection kanji, SentenceCollection sentences, JapaneseConfig config, DictLookup dictLookup, VocabNoteFactory vocabNoteFactory) =>
                                                        new LocalNoteUpdater(taskRunner, vocab, kanji, sentences, config, dictLookup, vocabNoteFactory)),
         Singleton.For<TaskRunner>().CreatedBy((JapaneseConfig config) => new TaskRunner(config)),
         Singleton.For<AnkiCardOperations>().CreatedBy(() => new AnkiCardOperations()),
         Singleton.For<TestApp>().CreatedBy((ConfigurationStore configurationStore) => new TestApp(app, configurationStore)),

         // Services owned by JPCollection — registered as property accessors
         Singleton.For<NoteServices>().CreatedBy((JPCollection col) => col.NoteServices),
         Singleton.For<DictLookup>().CreatedBy((JPCollection col) => col.DictLookup),
         Singleton.For<VocabNoteFactory>().CreatedBy((JPCollection col) => col.VocabNoteFactory),
         Singleton.For<VocabNoteGeneratedData>().CreatedBy((JPCollection col) => col.VocabNoteGeneratedData),
         Singleton.For<KanjiNoteMnemonicMaker>().CreatedBy((JapaneseConfig config) => new KanjiNoteMnemonicMaker(config)),

         // ViewModels
         Singleton.For<SentenceKanjiListViewModel>().CreatedBy((KanjiCollection kanji) => new SentenceKanjiListViewModel(kanji)),

         // Renderers
         Singleton.For<KanjiListRenderer>().CreatedBy((KanjiCollection kanji) => new KanjiListRenderer(kanji)),
         Singleton.For<VocabKanjiListRenderer>().CreatedBy((SentenceKanjiListViewModel vm) => new VocabKanjiListRenderer(vm)),
         Singleton.For<RelatedVocabsRenderer>().CreatedBy((VocabCollection vocab) => new RelatedVocabsRenderer(vocab)),
         Singleton.For<UdSentenceBreakdownRenderer>().CreatedBy((Settings settings, SentenceKanjiListViewModel vm, JapaneseConfig config, VocabCollection vocab) => new UdSentenceBreakdownRenderer(settings, vm, config, vocab)),
         Singleton.For<QuestionRenderer>().CreatedBy((JapaneseConfig config) => new QuestionRenderer(config)),
         Singleton.For<SentenceRenderer>().CreatedBy((JapaneseConfig config) => new SentenceRenderer(config)),

         // Note renderers
         Singleton.For<VocabNoteRenderer>().CreatedBy((RelatedVocabsRenderer relatedVocabs, VocabKanjiListRenderer vocabKanjiList) => new VocabNoteRenderer(relatedVocabs, vocabKanjiList)),
         Singleton.For<SentenceNoteRenderer>().CreatedBy((SentenceRenderer sentenceRenderer, UdSentenceBreakdownRenderer udRenderer) => new SentenceNoteRenderer(sentenceRenderer, udRenderer)),
         Singleton.For<KanjiNoteRenderer>().CreatedBy((KanjiListRenderer kanjiList) => new KanjiNoteRenderer(kanjiList))
      );

      TemporaryServiceCollection.Instance = container.ServiceLocator.Resolve<TemporaryServiceCollection>();
      return container.ServiceLocator;
   }
}
