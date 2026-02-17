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

static class AppBootstrapper
{
   internal static IServiceLocator Bootstrap(
      CoreApp coreApp,
      IBackendNoteCreator? backendNoteCreator = null,
      IBackendDataLoader? backendDataLoader = null)
   {
      backendNoteCreator ??= new TestingBackendNoteCreator();

      var container = new SimpleInjectorDependencyInjectionContainer();
      var registrar = container.Register();

      var paths = coreApp.Paths;

      if(CoreApp.IsTesting)
      {
         registrar.Register(
            Singleton.For<INoteRepository>().CreatedBy(() => (INoteRepository)new InMemoryNoteRepository()));
      } else
      {
         registrar.Register(
            Singleton.For<INoteRepository>().CreatedBy((NoteSerializer serializer, TaskRunner taskRunner) =>
                                                          (INoteRepository)new FileSystemNoteRepository(serializer, taskRunner, paths)));
      }

      registrar.Register(
         Singleton.For<IBackendNoteCreator>().Instance(backendNoteCreator),
         Singleton.For<CoreApp>().Instance(coreApp),
         Singleton.For<IEnvironmentPaths>().Instance(paths),
         Singleton.For<ConfigurationStore>().CreatedBy((TemporaryServiceCollection services) => new ConfigurationStore(paths)),
         Singleton.For<TemporaryServiceCollection>().CreatedBy(() => new TemporaryServiceCollection(container.ServiceLocator)),
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
         Singleton.For<TaskRunner>().CreatedBy((JapaneseConfig config) => new TaskRunner()),
         Singleton.For<CardOperations>().CreatedBy(() => new CardOperations()),
         Singleton.For<TestCoreApp>().CreatedBy((ConfigurationStore configurationStore) => new TestCoreApp(coreApp, configurationStore)),

         // Services owned by JPCollection — registered as property accessors
         Singleton.For<NoteServices>().CreatedBy(() => new NoteServices(container.ServiceLocator)),
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

      return container.ServiceLocator;
   }
}
