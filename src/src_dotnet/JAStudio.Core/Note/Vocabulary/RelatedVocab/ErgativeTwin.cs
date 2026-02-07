using System.Linq;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class ErgativeTwin
{
    private readonly VocabNote _vocab;
    private readonly MutableSerializedObjectField<RelatedVocabData> _data;

    public ErgativeTwin(VocabNote vocab, MutableSerializedObjectField<RelatedVocabData> data)
    {
        _vocab = vocab;
        _data = data;
    }

    public string Get() => _data.Get().ErgativeTwin;

    public void Set(string value)
    {
        _data.Get().ErgativeTwin = value;

        foreach (var twin in TemporaryServiceCollection.Instance.App.Col().Vocab.WithQuestion(value))
        {
            if (twin.RelatedNotes.ErgativeTwin.Get() != _vocab.GetQuestion())
            {
                twin.RelatedNotes.ErgativeTwin.Set(_vocab.GetQuestion());
            }
        }

        _data.Save();
    }

    public void Remove()
    {
        foreach (var twin in TemporaryServiceCollection.Instance.App.Col().Vocab.WithQuestion(_vocab.GetQuestion()))
        {
            if (twin.RelatedNotes.ErgativeTwin.Get() == _vocab.GetQuestion())
            {
                twin.RelatedNotes.ErgativeTwin.Remove();
            }
        }

        _data.Get().ErgativeTwin = string.Empty;

        _data.Save();
    }
}
