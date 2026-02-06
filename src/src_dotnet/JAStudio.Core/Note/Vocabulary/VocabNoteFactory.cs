using System;
using System.Collections.Generic;
using JAStudio.Core.LanguageServices.JamdictEx;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteFactory
{
   readonly TemporaryServiceCollection _services;
   internal VocabNoteFactory(TemporaryServiceCollection services) => _services = services;

    public static VocabNote CreateWithDictionary(string question)
    {
        var lookupResult = DictLookup.LookupWord(question);
        if (!lookupResult.FoundWords())
        {
            return Create(question, "", new List<string>());
        }

        var created = Create(question, lookupResult.FormatAnswer(), lookupResult.Readings());
        created.Tags.Set(Tags.Source.Jamdict);
        created.UpdateGeneratedData();
        return created;
    }

    public static VocabNote Create(string question, string answer, List<string> readings, Action<VocabNote>? initializer = null)
    {
        var note = new VocabNote();
        note.Question.Set(question);
        note.SetField(NoteFieldsConstants.Vocab.SourceAnswer, answer);
        note.SetReadings(readings);
        
        if (initializer != null)
        {
            initializer(note);
        }
        
        App.Col().Vocab.Add(note);
        return note;
    }

    public static VocabNote CreateFromUserData(string question, string answer, List<string> readings, Action<VocabNote>? initializer = null)
    {
        var note = Create(question, answer, readings, initializer);
        note.User.Answer.Set(note.GetField(NoteFieldsConstants.Vocab.SourceAnswer));
        note.SetField(NoteFieldsConstants.Vocab.SourceAnswer, "");
        
        return note;
    }
}
