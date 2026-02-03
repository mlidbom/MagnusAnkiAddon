using System;

namespace JAStudio.Core.Note.NoteFields;

public class RequireForbidFlagField
{
    private readonly JPNote _note;
    private readonly Tag _requiredTag;
    private readonly Tag _forbiddenTag;
    private readonly bool _cachedIsRequired;
    private readonly bool _cachedIsForbidden;

    public int RequiredWeight { get; }
    public int ForbiddenWeight { get; }

    public RequireForbidFlagField(JPNote note, int requiredWeight, int forbiddenWeight, Tag requiredTag, Tag forbiddenTag)
    {
        _note = note;
        _requiredTag = requiredTag;
        _forbiddenTag = forbiddenTag;
        RequiredWeight = requiredWeight;
        ForbiddenWeight = forbiddenWeight;
        
        // Cache tag states during construction - invalidated when matching_configuration is recreated
        _cachedIsRequired = note.Tags.Contains(requiredTag);
        _cachedIsForbidden = note.Tags.Contains(forbiddenTag);
    }

    public bool IsConfiguredRequired => _cachedIsRequired;
    public bool IsConfiguredForbidden => _cachedIsForbidden;
    
    public int MatchWeight => IsRequired ? RequiredWeight : IsForbidden ? ForbiddenWeight : 0;

    public string Name => _requiredTag.Name.Replace(Tags.Vocab.Matching.Requires.FolderName, "");

    public virtual bool IsRequired => _cachedIsRequired;
    public bool IsForbidden => _cachedIsForbidden;
    public bool IsActive => _cachedIsRequired || _cachedIsForbidden;

    public void SetForbidden(bool value)
    {
        if (value)
        {
            _note.Tags.Set(_forbiddenTag);
            _note.Tags.Unset(_requiredTag);
        }
        else
        {
            _note.Tags.Unset(_forbiddenTag);
        }
    }

    public void SetRequired(bool value)
    {
        if (value)
        {
            _note.Tags.Set(_requiredTag);
            _note.Tags.Unset(_forbiddenTag);
        }
        else
        {
            _note.Tags.Unset(_requiredTag);
        }
    }

    public override string ToString()
    {
        return $"{Name} required: {IsRequired}, forbidden: {IsForbidden}";
    }
}
