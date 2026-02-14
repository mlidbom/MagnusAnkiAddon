using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.CorpusData;

/// Base for corpus data types. Provides the bridge to the internal Dictionary&lt;string, string&gt;
/// that JPNote still requires.
public abstract class CorpusDataBase
{
   public NoteId Id { get; }
   public List<string> Tags { get; }

   protected CorpusDataBase(NoteId id, List<string> tags)
   {
      Id = id;
      Tags = tags;
   }

   /// Converts this typed data into the flat NoteData that JPNote constructors consume.
   public NoteData ToNoteData()
   {
      var fields = new Dictionary<string, string>();
      PopulateFields(fields);
      fields[MyNoteFields.JasNoteId] = Id.Value.ToString();
      return new NoteData(Id, fields, Tags);
   }

   protected abstract void PopulateFields(Dictionary<string, string> fields);
}
