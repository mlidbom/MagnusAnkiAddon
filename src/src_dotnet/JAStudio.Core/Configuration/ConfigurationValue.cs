using Compze.Utilities.SystemCE;
using System;
using System.Collections.Generic;

namespace JAStudio.Core.Configuration;

public static class ConfigurationValue
{
    private static Dictionary<string, object>? _configDictReal;
    private static Action<Dictionary<string, object>>? _updateCallback;

    public static void Init(Dictionary<string, object> configDict, Action<Dictionary<string, object>> updateCallback)
    {
        if (_configDictReal != null)
        {
            throw new InvalidOperationException("Configuration dict already initialized");
        }

        _configDictReal = configDict;
        _updateCallback = updateCallback;
    }

    private static Dictionary<string, object> GetConfigDict()
    {
        if (App.IsTesting)
        {
            return new Dictionary<string, object>();
        }
        
        if (_configDictReal == null)
        {
            throw new InvalidOperationException("Configuration dict not initialized");
        }
        
        return _configDictReal;
    }

    private static readonly LazyCE<Dictionary<string, object>> _configDict = new(GetConfigDict);

    private static void WriteConfigDict()
    {
        if (!App.IsTesting && _updateCallback != null && _configDictReal != null)
        {
            _updateCallback(_configDictReal);
        }
    }

    private static JapaneseConfig? _config;

    public static JapaneseConfig Config()
    {
        return _config ??= new JapaneseConfig();
    }
}

public class JapaneseConfig
{
    // Placeholder - configuration values will be added as needed
    public JapaneseConfig()
    {
        // TODO: Initialize configuration values
    }
}
