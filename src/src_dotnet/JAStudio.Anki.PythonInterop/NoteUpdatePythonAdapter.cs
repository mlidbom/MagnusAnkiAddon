using System;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.PythonInterop;

namespace JAStudio.Anki.PythonInterop;

/// <summary>
/// Adapts Python callable objects to typed .NET delegates for note update listeners.
/// </summary>
public static class NoteUpdatePythonAdapter
{
   /// <summary>
   /// Registers a Python callable as an update listener on an <see cref="IExternalNoteUpdateHandler"/>.
   /// Wraps the Python callable as an <see cref="Action{JPNote}"/> using PythonDotNetShim.
   /// </summary>
   // ReSharper disable once UnusedMember.Global used from python
   public static void Register(IExternalNoteUpdateHandler handler, dynamic pythonCallback)
   {
      Action<JPNote> typed = PythonDotNetShim.Action.ToDotNet<JPNote>(pythonCallback);
      handler.OnNoteUpdated(typed);
   }
}
