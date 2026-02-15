using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage.Converters;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note;

public class VocabNote : JPNote
{
    public VocabNoteQuestion Question { get; private set; }
    public MutableCommaSeparatedStringsListField Readings { get; }
    public VocabNoteUserFields User { get; }
    public VocabNoteForms Forms { get; }
    public VocabNoteKanji Kanji { get; }
    public VocabNotePartsOfSpeech PartsOfSpeech { get; }
    public VocabNoteConjugator Conjugator { get; }
    public VocabNoteSentences Sentences { get; }
    public VocabNoteUserCompoundParts CompoundParts { get; }
    public Vocabulary.RelatedVocab.RelatedVocab RelatedNotes { get; }
    public VocabNoteMetaData MetaData { get; }
    public VocabNoteRegister Register { get; }
    public VocabNoteAudio Audio { get; }
    public VocabNoteMatchingConfiguration MatchingConfiguration { get; private set; }
    public VocabCloner Cloner { get; }

    // Property accessors for fields
    public MutableStringField SourceAnswer => StringField(NoteFieldsConstants.Vocab.SourceAnswer);
    public MutableStringField ActiveAnswer => StringField(NoteFieldsConstants.Vocab.ActiveAnswer);
    public MutableStringField SourceMnemonic => StringField(NoteFieldsConstants.Vocab.SourceMnemonic);
    public MutableStringField SourceReadingMnemonic => StringField(NoteFieldsConstants.Vocab.SourceReadingMnemonic);
    public MutableStringField TechnicalNotes => StringField(NoteFieldsConstants.Vocab.TechnicalNotes);
    public MutableStringField References => StringField(NoteFieldsConstants.Vocab.References);
    public ImageField Image => new(StringField(NoteFieldsConstants.Vocab.Image));
    public ImageField UserImage => new(StringField(NoteFieldsConstants.Vocab.UserImage));

    public VocabNote(NoteServices services, VocabData? data = null) : base(services, data != null ? new VocabId(data.Id) : VocabId.New(), data?.ToNoteData())
    {
        Question = new VocabNoteQuestion(this, GetField, SetField);
        Readings = new MutableCommaSeparatedStringsListField(CachingStringField(NoteFieldsConstants.Vocab.Reading));
        User = new VocabNoteUserFields(this, GetField, SetField);
        Forms = new VocabNoteForms(this, GetField, SetField);
        Kanji = new VocabNoteKanji(this);
        PartsOfSpeech = new VocabNotePartsOfSpeech(this, GetField, SetField);
        Conjugator = new VocabNoteConjugator(this);
        Sentences = new VocabNoteSentences(this);
        CompoundParts = new VocabNoteUserCompoundParts(this, GetField, SetField);
        RelatedNotes = new Vocabulary.RelatedVocab.RelatedVocab(this, GetField, SetField);
        MetaData = new VocabNoteMetaData(this, GetField, SetField);
        Register = new VocabNoteRegister(this);
        Audio = new VocabNoteAudio(data, Guard);
        MatchingConfiguration = new VocabNoteMatchingConfiguration(this, GetField, SetField);
        Cloner = new VocabCloner(this);
    }

    public override void UpdateInCache()
    {
        Services.Collection.Vocab.Cache.JpNoteUpdated(this);
    }

    public override CorpusDataBase ToCorpusData() => VocabNoteConverter.ToCorpusData(this);

    public override string GetQuestion()
    {
        return Question.Raw;
    }

    public override List<MediaReference> GetMediaReferences()
    {
        var refs = Audio.First.GetMediaReferences();
        refs.AddRange(Audio.Second.GetMediaReferences());
        refs.AddRange(Audio.Tts.GetMediaReferences());
        refs.AddRange(Image.GetMediaReferences());
        refs.AddRange(UserImage.GetMediaReferences());
        return refs;
    }

    public override string GetAnswer()
    {
        var userAnswer = User.Answer.Value;
        var sourceAnswer = SourceAnswer.Value;
        return !string.IsNullOrEmpty(userAnswer) ? userAnswer : sourceAnswer;
    }

    public override HashSet<JPNote> GetDirectDependencies()
    {
        return RelatedNotes.GetDirectDependencies();
    }

    public override void OnTagsUpdated()
    {
        MatchingConfiguration = new VocabNoteMatchingConfiguration(this, GetField, SetField);
    }

    public override void UpdateGeneratedData()
    {
        base.UpdateGeneratedData();
        
        Services.VocabNoteGeneratedData.UpdateGeneratedData(this);
    }

    public List<string> GetReadings()
    {
        return Readings.Get();
    }

    public void SetReadings(List<string> readings)
    {
        Readings.Set(readings);
    }

    public void GenerateAndSetAnswer()
    {
        var dictLookup = Services.DictLookup.LookupVocabWordOrName(this);
        if (dictLookup.FoundWords())
        {
            var generated = dictLookup.FormatAnswer();
            SourceAnswer.Set(generated);
        }

        UpdateGeneratedData();
    }

    public static VocabNote Create(NoteServices services, string question, string answer, List<string> readings, List<string> forms)
    {
        var note = new VocabNote(services);
        note.Question.Set(question);
        note.User.Answer.Set(answer);
        note.SetReadings(readings);

        if(forms.Any())
        {
            note.Forms.SetList(forms);
        }

        note.UpdateGeneratedData();
        services.Collection.Vocab.Add(note);
        return note;
    }

    public static VocabNote Create(NoteServices services, string question, string answer, params string[] readings)
    {
        return Create(services, question, answer, readings.ToList(), new List<string>());
    }
}
