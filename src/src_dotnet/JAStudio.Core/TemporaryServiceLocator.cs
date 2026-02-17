using System;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Batches;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.UI.Web.Kanji;
using JAStudio.Core.UI.Web.Sentence;
using JAStudio.Core.UI.Web.Vocab;

namespace JAStudio.Core;

//TODO: We should redesign so that we have a sane dependency graph and just use normal dependency injection, but first we need to get rid of all the static classes and this will help us do that
public class TemporaryServiceCollection : IDisposable
{
   public static TemporaryServiceCollection Instance { get; internal set; } = null!;

   internal TemporaryServiceCollection(IServiceLocator serviceLocator) => ServiceLocator = serviceLocator;

   public CoreApp CoreApp => ServiceLocator.Resolve<CoreApp>();
   public ConfigurationStore ConfigurationStore => ServiceLocator.Resolve<ConfigurationStore>();

   // Core services
   public LocalNoteUpdater LocalNoteUpdater => ServiceLocator.Resolve<LocalNoteUpdater>();
   public TaskRunner TaskRunner => ServiceLocator.Resolve<TaskRunner>();
   public CardOperations CardOperations => ServiceLocator.Resolve<CardOperations>();
   public ExternalNoteIdMap ExternalNoteIdMap => ServiceLocator.Resolve<ExternalNoteIdMap>();

   // Note services
   public NoteServices NoteServices => ServiceLocator.Resolve<NoteServices>();
   public VocabNoteFactory VocabNoteFactory => ServiceLocator.Resolve<VocabNoteFactory>();

   public IServiceLocator ServiceLocator { get; }

   public Renderers Renderers => new Renderers(ServiceLocator);

   public void Dispose() => ServiceLocator.Dispose();
}

public class Renderers
{
   readonly IServiceLocator _serviceLocator;
   internal Renderers(IServiceLocator serviceLocator) => _serviceLocator = serviceLocator;

   public VocabNoteRenderer VocabNoteRenderer => _serviceLocator.Resolve<VocabNoteRenderer>();
   public SentenceNoteRenderer SentenceNoteRenderer => _serviceLocator.Resolve<SentenceNoteRenderer>();
   public KanjiNoteRenderer KanjiNoteRenderer => _serviceLocator.Resolve<KanjiNoteRenderer>();
}
