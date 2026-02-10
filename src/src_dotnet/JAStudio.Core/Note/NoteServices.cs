using JAStudio.Core.Anki;
using JAStudio.Core.Configuration;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Note;

/// <summary>
/// Bundles all external services that notes and their composed objects need.
/// Passed to JPNote subclasses via their constructor so that notes and their
/// sub-objects can access services without going through the static service locator.
/// </summary>
public class NoteServices
{
   public JPCollection Collection { get; }
   public AnkiCardOperations AnkiCardOperations { get; }
   public Settings Settings { get; }
   public DictLookup DictLookup { get; }
   public VocabNoteFactory VocabNoteFactory { get; }
   public VocabNoteGeneratedData VocabNoteGeneratedData { get; }
   public KanjiNoteMnemonicMaker KanjiNoteMnemonicMaker { get; }
   public JapaneseConfig Config { get; }
   public TaskRunner TaskRunner { get; }
   public AnkiNoteIdMap AnkiNoteIdMap { get; }

   internal NoteServices(
      JPCollection collection,
      AnkiCardOperations ankiCardOperations,
      Settings settings,
      DictLookup dictLookup,
      VocabNoteFactory vocabNoteFactory,
      VocabNoteGeneratedData vocabNoteGeneratedData,
      KanjiNoteMnemonicMaker kanjiNoteMnemonicMaker,
      JapaneseConfig config,
      TaskRunner taskRunner,
      AnkiNoteIdMap ankiNoteIdMap)
   {
      Collection = collection;
      AnkiCardOperations = ankiCardOperations;
      Settings = settings;
      DictLookup = dictLookup;
      VocabNoteFactory = vocabNoteFactory;
      VocabNoteGeneratedData = vocabNoteGeneratedData;
      KanjiNoteMnemonicMaker = kanjiNoteMnemonicMaker;
      Config = config;
      TaskRunner = taskRunner;
      AnkiNoteIdMap = ankiNoteIdMap;
   }
}
