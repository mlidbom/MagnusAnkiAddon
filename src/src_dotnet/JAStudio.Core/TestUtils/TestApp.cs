using JAStudio.Core.Note;
using System;

namespace JAStudio.Core.TestUtils;

public static class TestApp
{
    private static bool _isInitialized;

    public static void Initialize()
    {
        if (_isInitialized)
        {
            return;
        }

        ExPytest.IsTesting = true;
        App.Reset(new TestingBackendNoteCreator());
        
        _isInitialized = true;
    }

    public static void Reset()
    {
        App.Reset(new TestingBackendNoteCreator());
    }
}
