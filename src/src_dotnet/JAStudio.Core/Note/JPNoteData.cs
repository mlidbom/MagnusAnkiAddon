using System;
using System.Collections.Generic;
using JAStudio.PythonInterop;
using JAStudio.PythonInterop.Utilities;

namespace JAStudio.Core.Note;

public class NoteData
{
   public NoteId? Id { get; set; }
   public Dictionary<string, string> Fields { get; set; }
   public List<string> Tags { get; set; }

   public NoteData(NoteId? id, Dictionary<string, string> fields, List<string> tags)
   {
      Id = id;
      Fields = fields;
      Tags = tags;
   }

   /// <summary>
   /// Creates NoteData from Python. The domain NoteId is NOT set here — it must be assigned
   /// by the caller (e.g. the sync handler or bulk loader) since Python only knows external IDs.
   /// </summary>
   public static NoteData FromPythonNoteData(dynamic item)
   {
      var fields = PythonDotNetShim.StringStringDict.ToDotNet(item.fields);
      var tags = PythonDotNetShim.StringList.ToDotNet(item.tags);
      return new NoteData(null, fields, tags);
   }

   //class JPNoteData:
   // def __init__(self, id: JPNoteId, fields:dict[str, str], tags: list[str]) -> None:
   //     self.id: JPNoteId = id
   //     self.fields: dict[str, str] = fields
   //     self.tags: list[str] = tags
}
