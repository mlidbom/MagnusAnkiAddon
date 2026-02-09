using JAStudio.Core.Note.Collection;
using System;
using System.Collections.Generic;
using JAStudio.Core.LanguageServices.JamdictEx;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteFactory
{
   readonly DictLookup _dictLookup;
   readonly JPCollection _collection;
   NoteServices? _noteServices;

   internal VocabNoteFactory(DictLookup dictLookup, JPCollection collection)
   {
      _dictLookup = dictLookup;
      _collection = collection;
   }

   /// <summary>Called by JPCollection after NoteServices is created to complete the wiring.</summary>
   internal void SetNoteServices(NoteServices noteServices) => _noteServices = noteServices;
   NoteServices RequireServices() => _noteServices ?? throw new InvalidOperationException("NoteServices not set on VocabNoteFactory. Call SetNoteServices first.");

    public VocabNote CreateWithDictionary(string question)
    {
        var lookupResult = _dictLookup.LookupWord(question);
        if (!lookupResult.FoundWords())
        {
            return Create(question, "", new List<string>());
        }

        var created = Create(question, lookupResult.FormatAnswer(), lookupResult.Readings());
        created.Tags.Set(Tags.Source.Jamdict);
        created.UpdateGeneratedData();
        return created;
    }

    public VocabNote Create(string question, string answer, List<string> readings, Action<VocabNote>? initializer = null)
    {
        var note = new VocabNote(RequireServices());
        note.Question.Set(question);
        note.SetField(NoteFieldsConstants.Vocab.SourceAnswer, answer);
        note.SetReadings(readings);
        
        if (initializer != null)
        {
            initializer(note);
        }
        
        _collection.Vocab.Add(note);
        return note;
    }

    public VocabNote CreateFromUserData(string question, string answer, List<string> readings, Action<VocabNote>? initializer = null)
    {
        var note = Create(question, answer, readings, initializer);
        note.User.Answer.Set(note.GetField(NoteFieldsConstants.Vocab.SourceAnswer));
        note.SetField(NoteFieldsConstants.Vocab.SourceAnswer, "");
        
        return note;
    }
}
