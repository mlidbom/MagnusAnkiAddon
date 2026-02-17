using System.Text.RegularExpressions;
using JAStudio.Core.Note.Vocabulary;
using Xunit;

namespace JAStudio.Core.Specifications.Note.Vocabulary;

/// <summary>
/// Tests ported from test_vocabnote_misc.py
/// </summary>
public class VocabNoteMiscTests : SpecificationStartingWithAnEmptyCollection
{
   [Fact]
   public void FormsExclusionRegex()
   {
      var formsExclusions = new Regex(@"\[\[.*]]");
      Assert.Matches(formsExclusions, "[[らっしゃる]]");
   }

   [Fact]
   public void GenerateFromDictionary()
   {
      var vocab = GetService<VocabNoteFactory>().CreateWithDictionary("やる気満々");
      Assert.Equal("やる気満々", vocab.GetQuestion());
      Assert.Equal("totally-willing/fully-motivated", vocab.GetAnswer());
      Assert.Equal(["やるきまんまん"], vocab.GetReadings());
   }
}
