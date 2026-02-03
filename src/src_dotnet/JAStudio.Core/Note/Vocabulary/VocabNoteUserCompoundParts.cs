using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteUserCompoundParts
{
    private const string FieldName = "user_compounds"; // NoteFields.Vocab.user_compounds
    private readonly VocabNote _vocab;
    private readonly CommaSeparatedStringsListField _field;

    public VocabNoteUserCompoundParts(VocabNote vocab)
    {
        _vocab = vocab;
        _field = new CommaSeparatedStringsListField(vocab, FieldName);
    }

    private VocabNote Vocab => _vocab;

    public List<string> Primary()
    {
        return _field.Get()
            .Where(part => !part.StartsWith("["))
            .ToList();
    }

    public List<string> All()
    {
        return _field.Get()
            .Select(StripBrackets)
            .ToList();
    }

    public void Set(List<string> value)
    {
        _field.Set(value);
    }

    public HashSet<VocabNote> AllNotes()
    {
        return All()
            .SelectMany(part => App.Col().Vocab.WithQuestion(part))
            .ToHashSet();
    }

    public List<VocabNote> PrimaryPartsNotes()
    {
        return Primary()
            .SelectMany(part => App.Col().Vocab.WithFormPreferDisambiguationNameOrExactMatch(part))
            .ToList();
    }

    public void AutoGenerate()
    {
        // TODO: Implement when TextAnalysis and word extraction are ported
        // from jaslib.language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        // analysis = TextAnalysis(vocab.get_question(), ...)
        // compound_parts = [a.form for a in analysis.display_word_variants if a.form not in vocab.forms.all_set()]
        // ...
        // segments_missing_vocab = [segment for segment in compound_parts if not collection.vocab.is_word(segment)]
        // for missing in segments_missing_vocab:
        //     VocabNote.factory.create_with_dictionary(missing)
        // self.set(compound_parts)
    }

    private static string StripBrackets(string part)
    {
        return part.Replace("[", string.Empty).Replace("]", string.Empty);
    }

    public override string ToString()
    {
        return _field.ToString() ?? string.Empty;
    }
}
