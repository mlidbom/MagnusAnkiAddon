using JAStudio.Core.Note.CorpusData;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteAudio
{
    readonly NoteGuard _guard;
    string _first;
    string _second;
    string _tts;

    public WritableAudioValue First { get; }
    public WritableAudioValue Second { get; }
    public WritableAudioValue Tts { get; }

    public VocabNoteAudio(VocabData? data, NoteGuard guard)
    {
        _guard = guard;
        _first = data?.AudioB ?? string.Empty;
        _second = data?.AudioG ?? string.Empty;
        _tts = data?.AudioTTS ?? string.Empty;
        First = new WritableAudioValue(() => _first, value => _guard.Update(() => _first = value));
        Second = new WritableAudioValue(() => _second, value => _guard.Update(() => _second = value));
        Tts = new WritableAudioValue(() => _tts, value => _guard.Update(() => _tts = value));
    }

    public string PrimaryAudioPath
    {
        get
        {
            var firstPath = First.FirstAudioFilePath();
            if (!string.IsNullOrEmpty(firstPath)) return firstPath;
        
            var secondPath = Second.FirstAudioFilePath();
            if (!string.IsNullOrEmpty(secondPath)) return secondPath;
        
            var ttsPath = Tts.FirstAudioFilePath();
            if (!string.IsNullOrEmpty(ttsPath)) return ttsPath;
        
            return string.Empty;
        }
    }

    public string PrimaryAudio
    {
        get
        {
            var firstValue = First.RawValue();
            if (!string.IsNullOrEmpty(firstValue)) return firstValue;
        
            var secondValue = Second.RawValue();
            if (!string.IsNullOrEmpty(secondValue)) return secondValue;
        
            var ttsValue = Tts.RawValue();
            if (!string.IsNullOrEmpty(ttsValue)) return ttsValue;
        
            return string.Empty;
        }
    }

    public override string ToString()
    {
        return $"first: {First}, second: {Second}, tts: {Tts}";
    }
}
