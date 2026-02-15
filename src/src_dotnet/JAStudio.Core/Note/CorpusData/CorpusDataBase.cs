using System;
using System.Collections.Generic;
using MemoryPack;

namespace JAStudio.Core.Note.CorpusData;

/// Base for corpus data types. Provides the bridge to the flat NoteData
/// that JPNote still requires internally.
/// MemoryPack needs [MemoryPackUnion] for polymorphic base types.
[MemoryPackable(GenerateType.NoGenerate)]
[MemoryPackUnion(0, typeof(VocabData))]
[MemoryPackUnion(1, typeof(KanjiData))]
[MemoryPackUnion(2, typeof(SentenceData))]
public abstract partial class CorpusDataBase
{
   public Guid Id { get; init; }
   public List<string> Tags { get; init; } = [];

   protected abstract NoteId CreateTypedId();

   protected abstract void PopulateFields(Dictionary<string, string> fields);

   /// Converts this typed data into the flat NoteData that JPNote constructors consume.
   public NoteData ToNoteData()
   {
      var fields = new Dictionary<string, string>();
      PopulateFields(fields);
      fields[MyNoteFields.JasNoteId] = Id.ToString();
      return new NoteData(CreateTypedId(), fields, Tags);
   }

   /// Populates an existing dictionary with the current field values.
   public void PopulateInto(Dictionary<string, string> fields) => PopulateFields(fields);
}
