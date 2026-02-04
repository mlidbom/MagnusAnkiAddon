using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteRegister
{
    private readonly VocabNote _vocab;

    public VocabNoteRegister(VocabNote vocab)
    {
        _vocab = vocab;
    }

    private VocabNote Vocab => _vocab;

    public TagFlagField Polite => new TagFlagField(Vocab, Tags.Vocab.Register.Polite);
    public TagFlagField Formal => new TagFlagField(Vocab, Tags.Vocab.Register.Formal);
    public TagFlagField Informal => new TagFlagField(Vocab, Tags.Vocab.Register.Informal);
    public TagFlagField Archaic => new TagFlagField(Vocab, Tags.Vocab.Register.Archaic);
    public TagFlagField Sensitive => new TagFlagField(Vocab, Tags.Vocab.Register.Sensitive);
    public TagFlagField Vulgar => new TagFlagField(Vocab, Tags.Vocab.Register.Vulgar);
    public TagFlagField Humble => new TagFlagField(Vocab, Tags.Vocab.Register.Humble);
    public TagFlagField Literary => new TagFlagField(Vocab, Tags.Vocab.Register.Literary);
    public TagFlagField Honorific => new TagFlagField(Vocab, Tags.Vocab.Register.Honorific);
    public TagFlagField RoughMasculine => new TagFlagField(Vocab, Tags.Vocab.Register.RoughMasculine);`
    public TagFlagField SoftFeminine => new TagFlagField(Vocab, Tags.Vocab.Register.SoftFeminine);
    public TagFlagField Slang => new TagFlagField(Vocab, Tags.Vocab.Register.Slang);
    public TagFlagField Derogatory => new TagFlagField(Vocab, Tags.Vocab.Register.Derogatory);
    public TagFlagField Childish => new TagFlagField(Vocab, Tags.Vocab.Register.Childish);
}
