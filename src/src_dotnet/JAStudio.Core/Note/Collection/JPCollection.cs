namespace JAStudio.Core.Note.Collection;

public class JPCollection
{
    private readonly IBackendNoteCreator _backendNoteCreator;
    private bool _isInitialized;
    private bool _initializationStarted;

    public VocabCollection Vocab { get; }
    public KanjiCollection Kanji { get; }
    public SentenceCollection Sentences { get; }

    public JPCollection(IBackendNoteCreator backendNoteCreator)
    {
        _backendNoteCreator = backendNoteCreator;
        
        MyLog.Info("JPCollection.__init__");
        
        Vocab = new VocabCollection(backendNoteCreator);
        Kanji = new KanjiCollection(backendNoteCreator);
        Sentences = new SentenceCollection(backendNoteCreator);
    }

    public bool IsInitialized => _isInitialized;
}
