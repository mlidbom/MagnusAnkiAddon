using Compze.Utilities.Contracts;
using Compze.Utilities.DependencyInjection;
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
   public static CoreApp BootstrapProduction(IEnvironmentPaths environmentPaths, IBackendNoteCreator backendNoteCreator, IBackendDataLoader backendDataLoader) =>
      Bootstrap(environmentPaths, backendNoteCreator, backendDataLoader);

   public static CoreApp BootstrapForTests()
   {
      Assert.State.Is(CoreApp.IsTesting);

      var app = Bootstrap(new TestEnvironmentPaths(), new TestingBackendNoteCreator(), backendDataLoader: null);
      app.Services.ConfigurationStore.InitForTesting();
      app.Config.SetReadingsMappingsForTesting(TestReadingsMappings);
      return app;
   }

   static CoreApp Bootstrap(IEnvironmentPaths paths, IBackendNoteCreator backendNoteCreator, IBackendDataLoader? backendDataLoader)
   {
      var container = new SimpleInjectorDependencyInjectionContainer();
      var registrar = container.Register();

      registrar.Register(
         Singleton.For<INoteRepository>().CreatedBy((NoteSerializer serializer, TaskRunner taskRunner) =>
                                                       (INoteRepository)new FileSystemNoteRepository(serializer, taskRunner, paths)));

      registrar.Register(
         Singleton.For<IBackendNoteCreator>().Instance(backendNoteCreator),
         Singleton.For<IEnvironmentPaths>().Instance(paths),
         Singleton.For<CoreApp>().CreatedBy((TemporaryServiceCollection services) => new CoreApp(services, paths)),
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

      return container.ServiceLocator.Resolve<CoreApp>();
   }

   const string TestReadingsMappings = """
                                       aba:ABBA
                                       afu:afoo:t
                                       ai:eye
                                       akoga:a-couga:r
                                       ame:Ame:rican
                                       an:an:chovie
                                       asa:as-a
                                       ashi:ash
                                       ate:ate
                                       atsu:at-Sue
                                       ba:bu:tt
                                       baku:backu:p
                                       ban:bun
                                       bei:bay
                                       betsu:bets
                                       bi:bee
                                       bin:bin
                                       bo:bo:t
                                       bou:bow
                                       bu:bu:tt
                                       byou:BO
                                       chi:chi:mp
                                       chika:chick-a
                                       chiku:chick
                                       cho:cho:p
                                       chou:Chou
                                       chuu:chew
                                       da:DA
                                       dai:die
                                       dama:Dama:scus
                                       dan:done
                                       de:dea:d
                                       den:den
                                       do:do:g
                                       doku:dock
                                       dou:door
                                       e:E:lle
                                       ei:a:pe
                                       en:En:t
                                       fu:foo:t
                                       fuda:fooder
                                       fuku:fuck
                                       fun:fun
                                       futsu:foot's
                                       ga:gu:t
                                       gai:guy
                                       gan:gun
                                       gatsu:guts
                                       getsu:gets
                                       gi:GI
                                       giwa:give-a
                                       go:go:b
                                       gou:go
                                       gun:gun
                                       guu:goo
                                       gyou:gyo:za
                                       ha:hu:t
                                       habu:hub
                                       hada:had-a
                                       hai:hi:de
                                       haka:hacker
                                       haku:hack
                                       han:Hun
                                       hashi:hash
                                       he:hea:lth
                                       hei:hay
                                       heki:heck
                                       hen:hen
                                       hi:hi:t
                                       hiku:hicku:p
                                       hin:hin:t
                                       hiro:he-row
                                       hisa:hiss-a
                                       hitsu:hits
                                       hoo:haw
                                       hou:haw
                                       i:ea:gle
                                       iku:ick
                                       in:inn
                                       ino:inno:vation
                                       ita:Ita:ly
                                       itona:<read>i</read>n<read>tona</read>tion
                                       ji:ji:g
                                       jin:gin
                                       jo:Jo
                                       jou:jaw
                                       ju:ju:g
                                       jutsu:nin<read>jutsu</read>
                                       juu:je:wel
                                       ka:cu:t
                                       kai:kay:ak
                                       kaku:cack:le
                                       kame:came
                                       kan:can
                                       kane:canne:lloni
                                       kara:Cara
                                       kare:curry
                                       kasu:cuss
                                       kata:kata
                                       katsu:cuts
                                       kawa:Kawa:saki
                                       kayu:<read>ca</read>n-<read>you</read>
                                       ke:ke:ttle
                                       kei:ca:ke
                                       ketsu:ketsu:p
                                       ki:key
                                       kichi:kitche:n
                                       kimo:kimo:no
                                       kin:kin
                                       kitsu:kits
                                       ko:KO
                                       kokoroyo:Kokoroyo
                                       koku:cock
                                       koma:coma
                                       kon:con
                                       kona:con-a
                                       koto:koto
                                       kou:caw
                                       kowa:cowa:rd
                                       ku:coo:k
                                       kuku:cuckoo
                                       kura:curra:nt
                                       kuru:curry
                                       kuu:coo
                                       kyou:Kyou:to
                                       kyuu:cue
                                       ma:mu:t
                                       machi:match
                                       mai:mi:ce
                                       maji:magi:c
                                       maku:muck
                                       mamo:mamo:gram
                                       man:man
                                       maru:ma-rue
                                       masu:muss
                                       mata:mata:dor
                                       matsu:mutts
                                       mei:may
                                       metsu:met-Sue
                                       mi:mi:tt
                                       miso:miso
                                       mitsu:mitts
                                       mo:mo:p
                                       mochi:mochi
                                       moku:mock
                                       moo:maw
                                       moto:moto:r
                                       mou:maw
                                       moude:moude
                                       mugi:muggy
                                       muku:muck
                                       na:nu:t
                                       nan:nun
                                       nani:nun-y
                                       nano:nano
                                       ne:ne:t
                                       nega:nega:tion
                                       nichi:Nietzche
                                       no:kno:t
                                       noo:gnaw
                                       nou:gnaw
                                       nu:nu:de
                                       nyuu:new
                                       oda:awe-da:d
                                       odo:odo:meter
                                       odoro:odor
                                       omo:c<read>ommo</read>n
                                       on:on
                                       ona:on-a
                                       oo:awe
                                       oto:auto
                                       otsu:oats
                                       ou:awe
                                       pa:pa
                                       pai:pie
                                       pan:pun:t
                                       pi:pi:t
                                       po:po:t
                                       ppa:pa
                                       rai:rye
                                       raku:lucky
                                       ran:run
                                       rei:ray
                                       ri:ri:p
                                       rin:rin:g
                                       ro:ro:t
                                       ru:rue
                                       ryuu:dragon
                                       sa:su:d
                                       sai:cy:borg
                                       saida:aid-a
                                       saka:sucker
                                       saki:sucky
                                       saku:suck
                                       san:sun
                                       satsu:satsu:ma
                                       se:se:x
                                       sei:sa:bre
                                       seki:sexy
                                       sen:cen:taur
                                       setsu:sets
                                       sha:sha:ft
                                       shaku:shack
                                       shi:shi:t
                                       shiki:sheik-y
                                       shin:shin
                                       shino:shino:bu
                                       shita:shitter
                                       shitsu:Shih-Tzu
                                       sho:sho:t
                                       shoku:shock
                                       shou:shou:gun
                                       shutsu:shuts
                                       shuu:shoe
                                       so:so:t
                                       soda:sawdu:st
                                       soku:sock
                                       son:son
                                       sou:saw
                                       su:soo:t
                                       sui:swee:t
                                       suki:ski
                                       suko:Sco:t
                                       suku:suck
                                       suu:sue
                                       tai:tie
                                       taku:tack
                                       tame:tame
                                       tan:tan
                                       tazu:taze-u
                                       tei:ta:pe
                                       teki:techie
                                       ten:ten:t
                                       to:to:t
                                       tobira:to-be-ra:ther
                                       ton:ton:s
                                       too:toe
                                       tori:tory
                                       totsu:tots
                                       tou:toe
                                       tsu:tsu:n
                                       tsubu:<read>tsu</read>ndere-<read>bu</read>ll
                                       tsuka:Tsuka
                                       tsuu:two
                                       u:U:ber
                                       ura:ura:nium
                                       wa:wa:d
                                       waka:walker
                                       wan:one
                                       wari:warri:or
                                       wata:water
                                       ya:yu:ck
                                       yaku:yak
                                       yo:ya:cht
                                       yoku:yolk
                                       you:you:ghurt
                                       yuru:you-rue
                                       yuu:you:th
                                       zai:xy:lophone
                                       zan:Zan:sibar
                                       zo:zo:mbie
                                       zoku:zock
                                       zou:zou:mbie
                                       zu:Zeu:s
                                       """;
}
