using System;
using JAStudio.Anki;
using JAStudio.Core;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.TaskRunners;
using JAStudio.UI.Dialogs;

namespace JAStudio.UI.Utils;

/// <summary>
/// Production dependencies for running inside Anki with Avalonia UI.
/// </summary>
class AnkiBootstrapDependencies(string configJson, Action<string> configUpdateCallback) : IBootstrapDependencies
{
   public IEnvironmentPaths EnvironmentPaths { get; } = new AnkiEnvironmentPaths();
   public IBackendNoteCreator BackendNoteCreator { get; } = new AnkiBackendNoteCreator();
   public IBackendDataLoader BackendDataLoader { get; } = new AnkiBackendDataLoader();
   public IFatalErrorHandler FatalErrorHandler { get; } = new AvaloniaFatalErrorHandler();
   public ITaskProgressUI TaskProgressUI { get; } = new AvaloniaTaskProgressUI();
   public IConfigDictSource ConfigDictSource { get; } = new AnkiConfigDictSource(configJson, configUpdateCallback);
   public IReadingsMappingsSource? ReadingsMappingsSource => null;
   public Func<ExternalNoteIdMap, ICardOperations> CardOperationsFactory { get; } = idMap => new AnkiCardOperationsImpl(idMap);
}
