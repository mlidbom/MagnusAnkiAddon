namespace JAStudio.Core.Anki;

/// <summary>
/// Events from the Anki host that affect the .NET addon lifecycle.
/// Python forwards these via JAStudioAppRoot.HandleAnkiLifecycleEvent().
/// </summary>
public enum AnkiLifecycleEvent
{
   /// <summary>Anki profile opened and collection is available. Load/reload all data from the DB.</summary>
   ProfileOpened,

   /// <summary>Anki profile is about to close. Clear caches.</summary>
   ProfileClosing,

   /// <summary>Anki sync is about to start. The DB may become unreliable.</summary>
   SyncStarting,

   /// <summary>Anki sync completed. Reload caches from the (possibly changed) DB.</summary>
   SyncCompleted,

   /// <summary>A new Anki collection object was loaded (e.g. after sync). Reload caches.</summary>
   CollectionLoaded
}
