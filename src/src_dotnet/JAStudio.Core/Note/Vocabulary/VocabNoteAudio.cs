using System;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteAudio
{
    private readonly Func<VocabNote> _vocab;

    public VocabNoteAudio(Func<VocabNote> vocab)
    {
        _vocab = vocab;
        // TODO: Implement WritableAudioField when audio_field.py is ported
        // First = new WritableAudioField(vocab, NoteFields.Vocab.Audio_b);
        // Second = new WritableAudioField(vocab, NoteFields.Vocab.Audio_g);
        // Tts = new WritableAudioField(vocab, NoteFields.Vocab.Audio_TTS);
    }

    private VocabNote Vocab => _vocab();

    // TODO: Implement audio fields when WritableAudioField is ported
    // public WritableAudioField First { get; }
    // public WritableAudioField Second { get; }
    // public WritableAudioField Tts { get; }

    public string GetPrimaryAudioPath()
    {
        // TODO: Implement when audio fields are ported
        // return First.FirstAudiofilePath() ?? Second.FirstAudiofilePath() ?? Tts.FirstAudiofilePath() ?? string.Empty;
        return string.Empty;
    }

    public string GetPrimaryAudio()
    {
        // TODO: Implement when audio fields are ported
        // return First.RawValue() ?? Second.RawValue() ?? Tts.RawValue() ?? string.Empty;
        return string.Empty;
    }

    public override string ToString()
    {
        // TODO: Implement when audio fields are ported
        return string.Empty; // $"first: {First}, second: {Second}, tts: {Tts}";
    }
}
