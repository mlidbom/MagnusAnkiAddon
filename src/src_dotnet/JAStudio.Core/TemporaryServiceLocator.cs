using System;
using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.Batches;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.TaskRunners;

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
   public ICardOperations CardOperations => ServiceLocator.Resolve<ICardOperations>();
   public ExternalNoteIdMap ExternalNoteIdMap => ServiceLocator.Resolve<ExternalNoteIdMap>();

   // Note services
   public NoteServices NoteServices => ServiceLocator.Resolve<NoteServices>();
   public VocabNoteFactory VocabNoteFactory => ServiceLocator.Resolve<VocabNoteFactory>();

   public IServiceLocator ServiceLocator { get; }

   // ReSharper disable once UnusedMember.Global used from python
   public AnkiHTMLRenderers AnkiHTMLRenderers => ServiceLocator.Resolve<AnkiHTMLRenderers>();

   public void Dispose() => ServiceLocator.Dispose();
}