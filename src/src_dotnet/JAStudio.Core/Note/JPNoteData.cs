using System.Collections.Generic;
using JAStudio.PythonInterop;

namespace JAStudio.Core.Note;

public class NetNoteData
{
    public long Id { get; set; }
    public Dictionary<string, string> Fields { get; set; }
    public List<string> Tags { get; set; }

    public NetNoteData(long id, Dictionary<string, string> fields, List<string> tags)
    {
        Id = id;
        Fields = fields;
        Tags = tags;
    }

    public static IReadOnlyList<NetNoteData> FromPythonListOfNoteData(dynamic pythonList)
    {
       var result = new List<NetNoteData>();
       foreach(var item in pythonList)
       {
          result.Add(ToDotNet(item));
       }
       return result;
    }

    static NetNoteData ToDotNet(dynamic item)
    {
       var id = (long)item.id;
       var fields = PythonDotNetShim.StringStringDict.ToDotNet(item.fields);
       var tags = PythonDotNetShim.StringList.ToDotNet(item.tags);
       return new NetNoteData(id, fields, tags);
    }

    //class JPNoteData:
    // def __init__(self, id: JPNoteId, fields:dict[str, str], tags: list[str]) -> None:
    //     self.id: JPNoteId = id
    //     self.fields: dict[str, str] = fields
    //     self.tags: list[str] = tags
}
