namespace JAStudio.Core.Note.Collection;

public class JPCollection
{
    private readonly IBackendNoteCreator _backendNoteCreator;
    private bool _isInitialized;
    private bool _initializationStarted;

    public JPCollection(IBackendNoteCreator backendNoteCreator)
    {
        _backendNoteCreator = backendNoteCreator;
        
        MyLog.Info("JPCollection.__init__");
        
        // Collections will be initialized here
    }

    public bool IsInitialized => _isInitialized;
}
