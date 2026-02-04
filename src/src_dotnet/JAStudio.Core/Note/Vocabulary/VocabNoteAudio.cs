using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteAudio
{
    private readonly VocabNote _vocab;
    public WritableAudioField First { get; }
    public WritableAudioField Second { get; }
    public WritableAudioField Tts { get; }

    public VocabNoteAudio(VocabNote vocab)
    {
        _vocab = vocab;
        First = new WritableAudioField(vocab, NoteFieldsConstants.Vocab.Audio);
        Second = new WritableAudioField(vocab, NoteFieldsConstants.Vocab.Audio);  // Using same field - Python has Audio_b/Audio_g but C# might consolidate
        Tts = new WritableAudioField(vocab, NoteFieldsConstants.Vocab.Audio);
    }

    private VocabNote Vocab => _vocab;

    public string GetPrimaryAudioPath()
    {
        var firstPath = First.FirstAudioFilePath();
        if (!string.IsNullOrEmpty(firstPath)) return firstPath;
        
        var secondPath = Second.FirstAudioFilePath();
        if (!string.IsNullOrEmpty(secondPath)) return secondPath;
        
        var ttsPath = Tts.FirstAudioFilePath();
        if (!string.IsNullOrEmpty(ttsPath)) return ttsPath;
        
        return string.Empty;
    }

    public string GetPrimaryAudio()
    {
        var firstValue = First.RawValue();
        if (!string.IsNullOrEmpty(firstValue)) return firstValue;
        
        var secondValue = Second.RawValue();
        if (!string.IsNullOrEmpty(secondValue)) return secondValue;
        
        var ttsValue = Tts.RawValue();
        if (!string.IsNullOrEmpty(ttsValue)) return ttsValue;
        
        return string.Empty;
    }

    public override string ToString()
    {
        return $"first: {First}, second: {Second}, tts: {Tts}";
    }
}
