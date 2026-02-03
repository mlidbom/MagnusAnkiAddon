using JAStudio.Core.Note.NoteFields;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteForms
{
    private readonly VocabNote _vocab;
    private readonly CommaSeparatedStringsListField _field;

    public VocabNoteForms(VocabNote vocab)
    {
        _vocab = vocab;
        _field = new CommaSeparatedStringsListField(vocab, NoteFieldsConstants.Vocab.UserForms);
    }

    public List<string> AllList()
    {
        return _field.Get().Select(StripBrackets).ToList();
    }

    public HashSet<string> AllSet()
    {
        return AllList().ToHashSet();
    }

    public string AllRawString()
    {
        return _field.RawStringValue();
    }

    public List<VocabNote> AllListNotes()
    {
        return AllList()
            .SelectMany(form => App.Col().Vocab.Cache.WithQuestion(form))
            .ToList();
    }

    public HashSet<string> OwnedForms()
    {
        var owned = new HashSet<string> { _vocab.GetQuestion() };
        
        foreach (var form in _field.Get())
        {
            if (form.StartsWith("["))
            {
                owned.Add(StripBrackets(form));
            }
        }
        
        return owned;
    }

    public bool IsOwnedForm(string form)
    {
        return OwnedForms().Contains(form);
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

        // Also remove from notes that have this vocab's question as a form (use ToList to avoid modification during iteration)
        var removeNotes = App.Col().Vocab.Cache.WithQuestion(remove)
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

        // Also add to notes that reference this form (use ToList to avoid modification during iteration)
        var addNotes = App.Col().Vocab.Cache.WithQuestion(add)
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
