using System.Collections.Generic;
using JAStudio.PythonInterop;
using JAStudio.PythonInterop.Utilities;

namespace JAStudio.Core.Note;

public class NoteData
{
   public long Id { get; set; }
   public Dictionary<string, string> Fields { get; set; }
   public List<string> Tags { get; set; }

   public NoteData(long id, Dictionary<string, string> fields, List<string> tags)
   {
      Id = id;
      Fields = fields;
      Tags = tags;
   }

   public static IReadOnlyList<NoteData> FromPythonListOfNoteData(dynamic pythonList) => PythonEnvironment.Use(() =>
   {
      var result = new List<NoteData>();
      foreach(var item in pythonList)
      {
         result.Add(FromPythonNoteData(item));
      }

      return result;
   });

   public static NoteData FromPythonNoteData(dynamic item)
   {
      var id = (long)item.id;
      var fields = PythonDotNetShim.StringStringDict.ToDotNet(item.fields);
      var tags = PythonDotNetShim.StringList.ToDotNet(item.tags);
      return new NoteData(id, fields, tags);
   }

   //class JPNoteData:
   // def __init__(self, id: JPNoteId, fields:dict[str, str], tags: list[str]) -> None:
   //     self.id: JPNoteId = id
   //     self.fields: dict[str, str] = fields
   //     self.tags: list[str] = tags
}
