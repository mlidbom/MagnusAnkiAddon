using Compze.Utilities.Contracts;
using Compze.Utilities.DependencyInjection;
using Compze.Utilities.DependencyInjection.Abstractions;
using Compze.Utilities.DependencyInjection.SimpleInjector;
using JAStudio.Core.Batches;
using JAStudio.Core.Configuration;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.LanguageServices.JanomeEx;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage;
using JAStudio.Core.Storage.Media;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.TestUtils;
using JAStudio.Core.UI.Web.Kanji;
using JAStudio.Core.UI.Web.Sentence;
using JAStudio.Core.UI.Web.Vocab;
using JAStudio.Core.ViewModels.KanjiList;

namespace JAStudio.Core;

public static class AppBootstrapper
{
   public static CoreApp BootstrapProduction(
      IEnvironmentPaths environmentPaths,
      IBackendNoteCreator backendNoteCreator,
      IBackendDataLoader backendDataLoader,
      string configJson,
      System.Action<string> configUpdateCallback) =>
      Bootstrap(environmentPaths, backendNoteCreator, backendDataLoader,
         configDictSource: new AnkiConfigDictSource(configJson, configUpdateCallback));

   public static CoreApp BootstrapForTests()
   {
      Assert.State.Is(CoreApp.IsTesting);

      return Bootstrap(new TestEnvironmentPaths(), new TestingBackendNoteCreator(), backendDataLoader: null,
         readingsMappingsSource: new TestReadingsMappingsSource(),
         configDictSource: new TestConfigDictSource());
   }

   static CoreApp Bootstrap(
      IEnvironmentPaths paths,
      IBackendNoteCreator backendNoteCreator,
      IBackendDataLoader? backendDataLoader,
      IConfigDictSource? configDictSource = null,
      IReadingsMappingsSource? readingsMappingsSource = null)
   {
      configDictSource ??= new TestConfigDictSource();
      readingsMappingsSource ??= new FileReadingsMappingsSource(paths);
      var container = new SimpleInjectorDependencyInjectionContainer();
      var registrar = container.Register();

      registrar.Register(
         Singleton.For<INoteRepository>().CreatedBy((NoteSerializer serializer, TaskRunner taskRunner) =>
                                                       (INoteRepository)new FileSystemNoteRepository(serializer, taskRunner, paths)));

      registrar.Register(
         Singleton.For<IBackendNoteCreator>().Instance(backendNoteCreator),
         Singleton.For<IEnvironmentPaths>().Instance(paths),
         Singleton.For<IServiceLocator>().CreatedBy(() => container.ServiceLocator),
         Singleton.For<AnkiHTMLRenderers>().CreatedBy((IServiceLocator serviceLocator) => new AnkiHTMLRenderers(serviceLocator)),
         Singleton.For<CoreApp>().CreatedBy((TemporaryServiceCollection services) => new CoreApp(services, paths)),
         Singleton.For<ConfigurationStore>().CreatedBy(() => new ConfigurationStore(readingsMappingsSource, configDictSource)),
         Singleton.For<TemporaryServiceCollection>().CreatedBy((IServiceLocator serviceLocator) => new TemporaryServiceCollection(serviceLocator)),
         Singleton.For<JapaneseConfig>().CreatedBy((ConfigurationStore store) => store.Config()),
         Singleton.For<JPCollection>().CreatedBy((NoteServices noteServices, JapaneseConfig config, INoteRepository noteRepository, MediaFileIndex mediaFileIndex) =>
                                                    new JPCollection(backendNoteCreator, noteServices, config, noteRepository, mediaFileIndex, backendDataLoader)),
         Singleton.For<VocabCollection>().CreatedBy((JPCollection col) => col.Vocab),
         Singleton.For<KanjiCollection>().CreatedBy((JPCollection col) => col.Kanji),
         Singleton.For<SentenceCollection>().CreatedBy((JPCollection col) => col.Sentences),

         // Media storage
         Singleton.For<MediaFileIndex>().CreatedBy((TaskRunner taskRunner) =>
                                                      new MediaFileIndex(paths, taskRunner)),
         Singleton.For<MediaStorageService>().CreatedBy((MediaFileIndex index) =>
                                                           new MediaStorageService(paths, index)),

         // Core services
         Singleton.For<Settings>().CreatedBy((JapaneseConfig config) => new Settings(config)),
         Singleton.For<AnalysisServices>().CreatedBy((VocabCollection vocab, DictLookup dictLookup, Settings settings) => new AnalysisServices(vocab, dictLookup, settings)),
         Singleton.For<ExternalNoteIdMap>().CreatedBy(() => new ExternalNoteIdMap()),
         Singleton.For<LocalNoteUpdater>().CreatedBy((TaskRunner taskRunner, VocabCollection vocab, KanjiCollection kanji, SentenceCollection sentences, JapaneseConfig config, DictLookup dictLookup, VocabNoteFactory vocabNoteFactory, FileSystemNoteRepository fileSystemNoteRepository) =>
                                                        new LocalNoteUpdater(taskRunner, vocab, kanji, sentences, config, dictLookup, vocabNoteFactory, fileSystemNoteRepository)),
         Singleton.For<TaskRunner>().CreatedBy(() => new TaskRunner()),
         Singleton.For<CardOperations>().CreatedBy(() => new CardOperations()),

         // Services owned by JPCollection — registered as property accessors
         Singleton.For<NoteServices>().CreatedBy((IServiceLocator serviceLocator) => new NoteServices(serviceLocator)),
         Singleton.For<DictLookup>().CreatedBy((JPCollection col) => col.DictLookup),
         Singleton.For<VocabNoteFactory>().CreatedBy((JPCollection col) => col.VocabNoteFactory),
         Singleton.For<VocabNoteGeneratedData>().CreatedBy((JPCollection col) => col.VocabNoteGeneratedData),
         Singleton.For<NoteSerializer>().CreatedBy((NoteServices noteServices) => new NoteSerializer(noteServices)),
         Singleton.For<FileSystemNoteRepository>().CreatedBy((NoteSerializer serializer, TaskRunner taskRunner) =>
                                                                new FileSystemNoteRepository(serializer, taskRunner, paths)),
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

      return container.ServiceLocator.Resolve<CoreApp>();
   }
}
