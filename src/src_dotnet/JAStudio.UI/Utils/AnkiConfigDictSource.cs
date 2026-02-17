using System;
using System.Collections.Generic;
using JAStudio.Core.Configuration;
using Newtonsoft.Json;

namespace JAStudio.UI.Utils;

public class AnkiConfigDictSource : IConfigDictSource
{
   readonly Dictionary<string, object> _configDict;
   readonly Action<string> _updateCallback;

   public AnkiConfigDictSource(string json, Action<string> updateCallback)
   {
      _configDict = JsonConvert.DeserializeObject<Dictionary<string, object>>(json) ?? new Dictionary<string, object>();
      _updateCallback = updateCallback;
   }

   public Dictionary<string, object> Load() => _configDict;

   public void Persist(string json) => _updateCallback(json);
}
