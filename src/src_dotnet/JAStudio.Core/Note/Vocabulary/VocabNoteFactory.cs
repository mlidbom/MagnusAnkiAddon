using System;
using System.Collections.Generic;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteFactory
{
   readonly DictLookup _dictLookup;
   readonly JPCollection _collection;
   readonly NoteServices _noteServices;

   internal VocabNoteFactory(DictLookup dictLookup, JPCollection collection, NoteServices noteServices)
   {
      _dictLookup = dictLookup;
      _collection = collection;
      _noteServices = noteServices;
   }

    public VocabNote CreateWithDictionary(string question)
    {
        var lookupResult = _dictLookup.LookupWord(question);
        if (!lookupResult.FoundWords())
        {
            return Create(question, "", new List<string>());
        }

        var created = Create(question, lookupResult.FormatAnswer(), lookupResult.Readings(), note =>
        {
            note.Tags.Set(Tags.Source.Jamdict);
            note.UpdateGeneratedData();
        });
        return created;
    }

    public VocabNote Create(string question, string answer, List<string> readings, Action<VocabNote>? initializer = null)
    {
        var note = new VocabNote(_noteServices);
        using(note.RecursiveFlushGuard.PauseFlushing())
        {
            note.Question.Set(question);
            note.SetField(NoteFieldsConstants.Vocab.SourceAnswer, answer);
            note.SetReadings(readings);

            if(initializer != null)
            {
                initializer(note);
            }
        }

        _collection.Vocab.Add(note);
        return note;
    }

    public VocabNote CreateFromUserData(string question, string answer, List<string> readings, Action<VocabNote>? initializer = null)
    {
        var note = new VocabNote(_noteServices);
        using(note.RecursiveFlushGuard.PauseFlushing())
        {
            note.Question.Set(question);
            note.SetField(NoteFieldsConstants.Vocab.SourceAnswer, answer);
            note.SetReadings(readings);

            if(initializer != null)
            {
                initializer(note);
            }
        }

        _collection.Vocab.Add(note);

        note.User.Answer.Set(note.GetField(NoteFieldsConstants.Vocab.SourceAnswer));
        note.SetField(NoteFieldsConstants.Vocab.SourceAnswer, "");

        return note;
    }
}
