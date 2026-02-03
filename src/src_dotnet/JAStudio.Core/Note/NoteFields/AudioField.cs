using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.NoteFields;

public class AudioField
{
    protected readonly MutableStringField _field;

    public AudioField(JPNote note, string fieldName)
    {
        _field = new MutableStringField(note, fieldName);
    }

    public bool HasAudio()
    {
        return _field.Value.Trim().StartsWith("[sound:");
    }

    public string FirstAudioFilePath()
    {
        return HasAudio() ? AudioFilesPaths()[0] : string.Empty;
    }

    public string RawValue()
    {
        return _field.Value;
    }

    public List<string> AudioFilesPaths()
    {
        if (!HasAudio())
        {
            return new List<string>();
        }

        var strippedPaths = _field.Value.Trim().Replace("[sound:", "").Split(']');
        return strippedPaths.Select(path => path.Trim()).Where(path => !string.IsNullOrEmpty(path)).ToList();
    }

    public override string ToString()
    {
        return _field.ToString();
    }
}

public class WritableAudioField : AudioField
{
    public WritableAudioField(JPNote note, string fieldName) : base(note, fieldName)
    {
    }

    public void SetRawValue(string value)
    {
        _field.Set(value);
    }
}
