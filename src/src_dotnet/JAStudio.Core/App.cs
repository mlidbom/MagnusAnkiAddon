using JAStudio.Core.Configuration;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.TestUtils;
using System;
using System.Collections.Generic;
using System.IO;

namespace JAStudio.Core;

public class App
{
    public static bool IsTesting => ExPytest.IsTesting;

    private static JPCollection? _collection;
    private static IBackendNoteCreator? _backendNoteCreator;

    private static readonly List<Action> _initHooks = new();

    public static void AddInitHook(Action hook)
    {
        _initHooks.Add(hook);
    }

    public static JapaneseConfig Config()
    {
        return ConfigurationValue.Config();
    }

    public static JPCollection Col()
    {
        if (_collection == null)
        {
            if (_backendNoteCreator == null)
            {
                throw new Exception("Backend note creator not initialized");
            }
            _collection = new JPCollection(_backendNoteCreator);
        }
        return _collection;
    }

    public static void Reset(IBackendNoteCreator backendNoteCreator)
    {
        _collection = null;
        _backendNoteCreator = backendNoteCreator;
    }

    public static string UserFilesDir
    {
        get
        {
            var assemblyLocation = typeof(App).Assembly.Location;
            var assemblyDir = Path.GetDirectoryName(Path.GetDirectoryName(assemblyLocation)) ?? string.Empty;
            return Path.Combine(assemblyDir, "user_files");
        }
    }
}
