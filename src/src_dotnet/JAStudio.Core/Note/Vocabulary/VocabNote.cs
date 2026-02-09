using JAStudio.Core.Note.ReactiveProperties;
using JAStudio.Core.Note.Vocabulary;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note;

public class VocabNote : JPNote
{
    readonly PropertyBag _properties = new();

    // String properties registered in the PropertyBag
    public StringProperty SourceAnswer { get; }
    public StringProperty ActiveAnswer { get; }

    // Sub-objects (most now accept StringProperty from the PropertyBag)
    public VocabNoteQuestion Question { get; private set; }
    public CommaSeparatedListProperty Readings { get; }
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

    public VocabNote(NoteServices services, NoteData? data = null) : base(services, data?.Id != null ? new VocabId(data.Id.Value) : VocabId.New(), data)
    {
        // Register all string fields
        var questionField = _properties.String(NoteFieldsConstants.Vocab.Question);
        SourceAnswer = _properties.String(NoteFieldsConstants.Vocab.SourceAnswer);
        ActiveAnswer = _properties.String(NoteFieldsConstants.Vocab.ActiveAnswer);
        var userAnswer = _properties.String(NoteFieldsConstants.Vocab.UserAnswer);
        var userExplanation = _properties.String(NoteFieldsConstants.Vocab.UserExplanation);
        var userExplanationLong = _properties.String(NoteFieldsConstants.Vocab.UserExplanationLong);
        var userMnemonic = _properties.String(NoteFieldsConstants.Vocab.UserMnemonic);
        var userCompounds = _properties.String(NoteFieldsConstants.Vocab.UserCompounds);
        var readingField = _properties.String(NoteFieldsConstants.Vocab.Reading);
        var formsField = _properties.String(NoteFieldsConstants.Vocab.Forms);
        var partsOfSpeechField = _properties.String(NoteFieldsConstants.Vocab.PartsOfSpeech);
        var sourceMnemonic = _properties.String(NoteFieldsConstants.Vocab.SourceMnemonic);
        var audioB = _properties.String(NoteFieldsConstants.Vocab.AudioB);
        var audioG = _properties.String(NoteFieldsConstants.Vocab.AudioG);
        var audioTTS = _properties.String(NoteFieldsConstants.Vocab.AudioTTS);
        var kanjiField = _properties.String(NoteFieldsConstants.Vocab.Kanji);
        var sourceReadingMnemonic = _properties.String(NoteFieldsConstants.Vocab.SourceReadingMnemonic);
        var homophones = _properties.String(NoteFieldsConstants.Vocab.Homophones);
        var parsedTOS = _properties.String(NoteFieldsConstants.Vocab.ParsedTypeOfSpeech);
        var sentenceCountField = _properties.String(NoteFieldsConstants.Vocab.SentenceCount);
        var matchingRulesField = _properties.String(NoteFieldsConstants.Vocab.MatchingRules);
        var relatedVocabField = _properties.String(NoteFieldsConstants.Vocab.RelatedVocab);

        // Load all registered properties from Anki field dictionary
        _properties.LoadFromDictionary(data?.Fields);

        // Build sub-objects
        Question = new VocabNoteQuestion(this, questionField);
        Readings = new CommaSeparatedListProperty(readingField);
        User = new VocabNoteUserFields(userAnswer, userMnemonic, userExplanation, userExplanationLong);
        Forms = new VocabNoteForms(this, formsField);
        Kanji = new VocabNoteKanji(this);
        PartsOfSpeech = new VocabNotePartsOfSpeech(this, partsOfSpeechField);
        Conjugator = new VocabNoteConjugator(this);
        Sentences = new VocabNoteSentences(this);
        CompoundParts = new VocabNoteUserCompoundParts(this, userCompounds);
        RelatedNotes = new Vocabulary.RelatedVocab.RelatedVocab(this, relatedVocabField);
        MetaData = new VocabNoteMetaData(this, sentenceCountField);
        Register = new VocabNoteRegister(this);
        Audio = new VocabNoteAudio(audioB, audioG, audioTTS);
        MatchingConfiguration = new VocabNoteMatchingConfiguration(this, matchingRulesField);
        Cloner = new VocabCloner(this);

        // Wire up PropertyBag changes to JPNote's Flush mechanism
        _properties.AnyChanged.Subscribe(() => Flush());
    }

    public override NoteData GetData() => new(GetId(), _properties.ToDictionary(), Tags.ToInternedStringList());

    public override void UpdateInCache()
    {
        Services.Collection.Vocab.Cache.JpNoteUpdated(this);
    }

    public override string GetQuestion()
    {
        return Question.Raw;
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
        MatchingConfiguration = new VocabNoteMatchingConfiguration(this, MatchingConfiguration.MatchingRulesField);
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
        
        if (forms.Any())
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
