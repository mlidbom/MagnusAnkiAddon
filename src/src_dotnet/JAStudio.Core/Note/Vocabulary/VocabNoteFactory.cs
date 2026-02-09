using JAStudio.Core.Note.Collection;
using System;
using System.Collections.Generic;
using JAStudio.Core.LanguageServices.JamdictEx;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteFactory
{
   readonly DictLookup _dictLookup;
   readonly VocabCollection _vocab;
   NoteServices? _noteServices;

   internal VocabNoteFactory(DictLookup dictLookup, VocabCollection vocab)
   {
      _dictLookup = dictLookup;
      _vocab = vocab;
   }

   public void SetNoteServices(NoteServices noteServices) => _noteServices = noteServices;
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
        note.SourceAnswer.Set(answer);
        note.SetReadings(readings);
        
        if (initializer != null)
        {
            initializer(note);
        }
        
        _vocab.Add(note);
        return note;
    }

    public VocabNote CreateFromUserData(string question, string answer, List<string> readings, Action<VocabNote>? initializer = null)
    {
        var note = Create(question, answer, readings, initializer);
        note.User.Answer.Set(note.SourceAnswer.Value);
        note.SourceAnswer.Empty();
        
        return note;
    }
}
