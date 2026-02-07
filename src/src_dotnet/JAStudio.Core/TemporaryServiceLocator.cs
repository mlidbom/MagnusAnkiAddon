using System;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Anki;
using JAStudio.Core.AnkiUtils;
using JAStudio.Core.Configuration;
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
public class TemporaryServiceCollection : IDisposable
{
   public static TemporaryServiceCollection Instance { get; internal set; } = null!;

   readonly IServiceLocator _serviceLocator;
   public TemporaryServiceCollection(IServiceLocator serviceLocator) => _serviceLocator = serviceLocator;

   public App App => _serviceLocator.Resolve<App>();
   public ConfigurationStore ConfigurationStore => _serviceLocator.Resolve<ConfigurationStore>();
   public Settings Settings => _serviceLocator.Resolve<Settings>();
   public QueryBuilder QueryBuilder => _serviceLocator.Resolve<QueryBuilder>();

   // Core services
   public LocalNoteUpdater LocalNoteUpdater => _serviceLocator.Resolve<LocalNoteUpdater>();
   public TaskRunner TaskRunner => _serviceLocator.Resolve<TaskRunner>();
   public AnkiCardOperations AnkiCardOperations => _serviceLocator.Resolve<AnkiCardOperations>();
   public DictLookup DictLookup => _serviceLocator.Resolve<DictLookup>();

   // Note services
   public NoteServices NoteServices => _serviceLocator.Resolve<NoteServices>();
   public VocabNoteFactory VocabNoteFactory => _serviceLocator.Resolve<VocabNoteFactory>();

   public IServiceLocator ServiceLocator => _serviceLocator;

   public void Dispose() => _serviceLocator.Dispose();
}
