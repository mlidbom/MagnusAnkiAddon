using Compze.Utilities.SystemCE;
using JAStudio.Core.Note.NoteFields;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteForms
{
    private readonly VocabNote _vocab;
    private readonly MutableCommaSeparatedStringsListFieldDeDuplicated _field;
    private readonly LazyCE<HashSet<string>> _allRawSet;
    private readonly LazyCE<List<string>> _allList;
    private readonly LazyCE<HashSet<string>> _allSet;
    private readonly LazyCE<HashSet<string>> _ownedForms;
    private readonly LazyCE<HashSet<string>> _notOwnedByOtherVocab;

    public VocabNoteForms(VocabNote vocab)
    {
        _vocab = vocab;
        _field = new MutableCommaSeparatedStringsListFieldDeDuplicated(vocab, NoteFieldsConstants.Vocab.Forms);
        
        _allRawSet = new LazyCE<HashSet<string>>(() => _field.Get().ToHashSet());
        _allList = _field.LazyReader(() => _field.Get().Select(StripBrackets).ToList());
        _allSet = _field.LazyReader(() => _allList.Value.ToHashSet());
        _ownedForms = _field.LazyReader(ComputeOwnedForms);
        _notOwnedByOtherVocab = _field.LazyReader(ComputeNotOwnedByOtherVocab);
    }

    private HashSet<string> ComputeOwnedForms()
    {
        var owned = new HashSet<string> { _vocab.GetQuestion() };
        foreach (var form in _allRawSet.Value)
        {
            if (form.StartsWith("["))
            {
                owned.Add(StripBrackets(form));
            }
        }
        return owned;
    }

    private HashSet<string> ComputeNotOwnedByOtherVocab()
    {
        bool IsNotOwnedByOtherFormNote(string form)
        {
            return !_vocab.Services.Collection.Vocab.Cache.WithQuestion(form)
                .Any(formOwningVocab => 
                    formOwningVocab != _vocab && 
                    formOwningVocab.Forms.AllSet().Contains(_vocab.GetQuestion()));
        }

        return _vocab.Forms.AllSet()
            .Where(IsNotOwnedByOtherFormNote)
            .ToHashSet();
    }

    public bool IsOwnedForm(string form) => _ownedForms.Value.Contains(form);

    public HashSet<string> OwnedForms() => _ownedForms.Value;

    public List<string> AllList() => _allList.Value;
    public HashSet<string> AllSet() => _allSet.Value;
    public string AllRawString() => _field.RawStringValue();

    /// Returns all forms with brackets preserved (e.g. "[form]" stays as-is).
    public List<string> AllRawList() => _field.Get();

    public List<VocabNote> AllListNotes()
    {
        return _allList.Value
            .SelectMany(form => _vocab.Services.Collection.Vocab.Cache.WithQuestion(form))
            .ToList();
    }

    public List<VocabNote> AllListNotesBySentenceCount()
    {
        return AllListNotes()
            .OrderByDescending(vocab => vocab.Sentences.Counts().Total)
            .ToList();
    }

    public HashSet<string> NotOwnedByOtherVocab() => _notOwnedByOtherVocab.Value;

    public List<string> WithoutNoiseCharacters()
    {
        return AllList().Select(StripNoiseCharacters).ToList();
    }

    private static string StripNoiseCharacters(string input)
    {
        return input.Replace(Mine.VocabPrefixSuffixMarker, "");
    }

    private static string StripBrackets(string input)
    {
        return input.Replace("[", "").Replace("]", "");
    }

    public void SetSet(HashSet<string> forms)
    {
        SetList(forms.ToList());
    }

    public void SetList(List<string> forms)
    {
        _field.Set(forms);
    }

    public void Remove(string remove)
    {
        _field.Remove(remove);

        // Also remove from notes that have this vocab's question as a form
        var removeNotes = _vocab.Services.Collection.Vocab.Cache.WithQuestion(remove)
            .Where(voc => voc.Forms.AllSet().Contains(_vocab.GetQuestion()))
            .ToList();
        
        foreach (var removeNote in removeNotes)
        {
            removeNote.Forms.Remove(_vocab.GetQuestion());
        }
    }

    public void Add(string add)
    {
        _field.Add(add);

        // Also add to notes that reference this form
        var addNotes = _vocab.Services.Collection.Vocab.Cache.WithQuestion(add)
            .Where(voc => !voc.Forms.AllSet().Contains(_vocab.GetQuestion()))
            .ToList();
        
        foreach (var addNote in addNotes)
        {
            addNote.Forms.Add(_vocab.GetQuestion());
        }
    }

    public override string ToString()
    {
        return _field.ToString();
    }
}
