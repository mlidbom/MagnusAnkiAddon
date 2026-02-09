using JAStudio.Core.Note.ReactiveProperties;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteAudio
{
    public AudioProperty First { get; }
    public AudioProperty Second { get; }
    public AudioProperty Tts { get; }

    public VocabNoteAudio(StringProperty audioB, StringProperty audioG, StringProperty audioTTS)
    {
        First = new AudioProperty(audioB);
        Second = new AudioProperty(audioG);
        Tts = new AudioProperty(audioTTS);
    }

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
