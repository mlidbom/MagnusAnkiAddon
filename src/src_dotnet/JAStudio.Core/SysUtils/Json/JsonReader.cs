using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.SysUtils.Json;

/// <summary>
/// Simple JSON reader for deserializing dictionary data.
/// </summary>
public class JsonReader
{
    private readonly Dictionary<string, object> _data;

    public JsonReader(Dictionary<string, object> data)
    {
        _data = data;
    }

    public string GetString(string key)
    {
        return _data.TryGetValue(key, out var value) ? value?.ToString() ?? "" : "";
    }

    public int GetInt(string key)
    {
        if (_data.TryGetValue(key, out var value))
        {
            if (value is int intValue) return intValue;
            if (int.TryParse(value?.ToString(), out var parsed)) return parsed;
        }
        return 0;
    }

    public List<string> GetStringList(string key, List<string> defaultValue)
    {
        if (_data.TryGetValue(key, out var value) && value is List<object> list)
        {
            return list.Select(o => o.ToString() ?? "").ToList();
        }
        return defaultValue;
    }

    public List<T> GetObjectList<T>(string key, Func<JsonReader, T> factory, List<T> defaultValue)
    {
        if (_data.TryGetValue(key, out var value) && value is List<object> list)
        {
            return list.Select(o => factory(new JsonReader(o as Dictionary<string, object> ?? new Dictionary<string, object>()))).ToList();
        }
        return defaultValue;
    }
}

/// <summary>
/// Helper methods for JSON serialization and deserialization.
/// </summary>
public static class JsonHelper
{
    public static Dictionary<string, object> JsonToDict(string json)
    {
        // TODO: Implement proper JSON deserialization using System.Text.Json
        return new Dictionary<string, object>();
    }

    public static string DictToJson(Dictionary<string, object> dict)
    {
        // TODO: Implement proper JSON serialization using System.Text.Json
        return "{}";
    }
}
