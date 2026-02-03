using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Vocabulary;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note;

public class VocabNote : JPNote
{
    public VocabNoteQuestion Question { get; private set; }
    public CommaSeparatedStringsListField Readings { get; }
    public VocabNoteUserFields User { get; }
    public VocabNoteForms Forms { get; }
    public VocabNoteKanji Kanji { get; }
    public VocabNotePartsOfSpeech PartsOfSpeech { get; }

    public VocabNote(JPNoteData? data = null) : base(data)
    {
        Question = new VocabNoteQuestion(this);
        Readings = new CommaSeparatedStringsListField(this, NoteFieldsConstants.Vocab.ReadingKana);
        User = new VocabNoteUserFields(this);
        Forms = new VocabNoteForms(this);
        Kanji = new VocabNoteKanji(() => this);
        PartsOfSpeech = new VocabNotePartsOfSpeech(() => this);
    }

    public override void UpdateInCache()
    {
        App.Col().Vocab.Cache.JpNoteUpdated(this);
    }

    public override string GetQuestion()
    {
        return Question.Raw;
    }

    public override string GetAnswer()
    {
        var userAnswer = User.Answer.Value;
        var sourceAnswer = GetField(NoteFieldsConstants.Vocab.SourceAnswer);
        return !string.IsNullOrEmpty(userAnswer) ? userAnswer : sourceAnswer;
    }

    public override HashSet<JPNote> GetDirectDependencies()
    {
        // TODO: Implement related vocab dependencies when RelatedVocab is ported
        return new HashSet<JPNote>();
    }

    public override void UpdateGeneratedData()
    {
        base.UpdateGeneratedData();
        
        // Set active answer
        SetField(NoteFieldsConstants.Vocab.ActiveAnswer, GetAnswer());
        
        // TODO: Additional generated data updates when other components are ported
    }

    public List<string> GetReadings()
    {
        return Readings.Get();
    }

    public void SetReadings(List<string> readings)
    {
        Readings.Set(readings);
    }

    public static VocabNote Create(string question, string answer, List<string> readings, List<string> forms)
    {
        var note = new VocabNote();
        note.Question.Set(question);
        note.User.Answer.Set(answer);
        note.SetReadings(readings);
        
        if (forms.Any())
        {
            note.Forms.SetList(forms);
        }
        
        note.UpdateGeneratedData();
        App.Col().Vocab.Add(note);
        return note;
    }

    public static VocabNote Create(string question, string answer, params string[] readings)
    {
        return Create(question, answer, readings.ToList(), new List<string>());
    }
}
