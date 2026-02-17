using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.UI.Web.Vocab;

class CompoundPart
{
   public VocabNote VocabNote { get; set; }
   public int Depth { get; set; }

   public CompoundPart(VocabNote vocabNote, int depth = 0)
   {
      VocabNote = vocabNote;
      Depth = depth;
   }
}

public static class CompoundPartsRenderer
{
   static string CreateClasses(VocabNote vocab, int depth = 0)
   {
      var classes = string.Join(" ", vocab.GetMetaTags());
      classes += $" compound_part_depth_{depth}";
      return classes;
   }

   static string RenderVocabList(List<CompoundPart> vocabList, string title, string cssClass, bool reading = true)
   {
      string RenderReadings(CompoundPart vocabWrapper)
      {
         var vocabNote = vocabWrapper.VocabNote;
         var readings = string.Join(", ", vocabNote.GetReadings());
         return (reading && readings != vocabNote.Question.Raw)
                   ? $"""<span class="clipboard vocabReading">{readings}</span>"""
                   : "";
      }

      var vocabEntries = vocabList.Select(vocabWrapper => $$$"""
                                                             <div class="relatedVocab {{{CreateClasses(vocabWrapper.VocabNote, vocabWrapper.Depth)}}}">
                                                                 <audio src="{{{vocabWrapper.VocabNote.Audio.PrimaryAudioPath}}}"></audio><a class="play-button"></a>
                                                                 <span class="question clipboard">{{{vocabWrapper.VocabNote.Question.DisambiguationName}}}</span>
                                                                 {{{RenderReadings(vocabWrapper)}}}
                                                                 {{{vocabWrapper.VocabNote.MetaData.MetaTagsHtml(noSentenceStatistics: true)}}}
                                                                 <span class="meaning"> {{{vocabWrapper.VocabNote.GetAnswer()}}}</span>
                                                             </div>
                                                             """);

      return $$$"""
                 <div class="relatedVocabListDiv page_section {{{cssClass}}}">
                    <div class="page_section_title">{{{title}}}</div>
                    <div class="vocabHomophonesList">
                        <div>
                            {{{string.Join("\n", vocabEntries)}}}
                        </div>
                    </div>
                </div>
                """;
   }

   static List<CompoundPart> GetCompoundPartsRecursive(VocabNote vocabNote, int depth = 0, HashSet<NoteId>? visited = null)
   {
      visited ??= new HashSet<NoteId>();

      if(visited.Contains(vocabNote.GetId()))
         return new List<CompoundPart>();

      visited.Add(vocabNote.GetId());

      var compoundParts = vocabNote.CompoundParts.PrimaryPartsNotes();

      var result = new List<CompoundPart>();

      foreach(var part in compoundParts)
      {
         var wrapper = new CompoundPart(part, depth);
         result.Add(wrapper);
         var nestedParts = GetCompoundPartsRecursive(part, depth + 1, visited);
         result.AddRange(nestedParts);
      }

      return result;
   }

   public static string GenerateCompounds(VocabNote vocabNote)
   {
      var compoundParts = GetCompoundPartsRecursive(vocabNote);
      return compoundParts.Count > 0
                ? RenderVocabList(compoundParts, "compound parts", cssClass: "compound_parts")
                : "";
   }
}
