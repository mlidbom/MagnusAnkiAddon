using System.Collections.Generic;
using JAStudio.Core.Note.NoteFields.AutoSaveWrappers;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Note.Vocabulary.RelatedVocab;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.Note.Vocabulary;

public class RelatedVocabDataSerializerTests
{
    private readonly RelatedVocabDataSerializer _serializer;

    public RelatedVocabDataSerializerTests()
    {
        TestApp.Initialize();
        _serializer = RelatedVocabData.Serializer();
    }

    [Fact]
    public void EmptyObjectSerializesToEmptyString()
    {
        var emptyData = new RelatedVocabData(
            ergativeTwin: "",
            derivedFrom: new ValueWrapper<string>(""),
            perfectSynonyms: new HashSet<string>(),
            similar: new HashSet<string>(),
            antonyms: new HashSet<string>(),
            confusedWith: new HashSet<string>(),
            seeAlso: new HashSet<string>()
        );

        var result = _serializer.Serialize(emptyData);

        Assert.Equal("", result);
    }

    [Fact]
    public void DeserializeEmptyStringReturnsEmptyData()
    {
        var result = _serializer.Deserialize("");

        Assert.Equal("", result.ErgativeTwin);
        Assert.Equal("", result.DerivedFrom.Get());
        Assert.Empty(result.PerfectSynonyms);
        Assert.Empty(result.Synonyms);
        Assert.Empty(result.Antonyms);
        Assert.Empty(result.ConfusedWith);
        Assert.Empty(result.SeeAlso);
    }

    [Fact]
    public void RoundtripWithDataPreservesAllFields()
    {
        var original = new RelatedVocabData(
            ergativeTwin: "開く",
            derivedFrom: new ValueWrapper<string>("開ける"),
            perfectSynonyms: new HashSet<string> { "完璧", "完全" },
            similar: new HashSet<string> { "似ている", "同様" },
            antonyms: new HashSet<string> { "閉じる", "閉める" },
            confusedWith: new HashSet<string> { "明く" },
            seeAlso: new HashSet<string> { "開放", "開始" }
        );

        var serialized = _serializer.Serialize(original);
        var deserialized = _serializer.Deserialize(serialized);

        Assert.Equal("開く", deserialized.ErgativeTwin);
        Assert.Equal("開ける", deserialized.DerivedFrom.Get());
        Assert.Equal(new HashSet<string> { "完璧", "完全" }, deserialized.PerfectSynonyms);
        Assert.Equal(new HashSet<string> { "似ている", "同様" }, deserialized.Synonyms);
        Assert.Equal(new HashSet<string> { "閉じる", "閉める" }, deserialized.Antonyms);
        Assert.Equal(new HashSet<string> { "明く" }, deserialized.ConfusedWith);
        Assert.Equal(new HashSet<string> { "開放", "開始" }, deserialized.SeeAlso);
    }
}

public class VocabNoteMatchingRulesSerializerTests
{
    private readonly VocabNoteMatchingRulesSerializer _serializer;

    public VocabNoteMatchingRulesSerializerTests()
    {
        TestApp.Initialize();
        _serializer = new VocabNoteMatchingRulesSerializer();
    }

    [Fact]
    public void EmptyObjectSerializesToEmptyString()
    {
        var emptyData = new VocabNoteMatchingRulesData(
            surfaceIsNot: new HashSet<string>(),
            prefixIsNot: new HashSet<string>(),
            suffixIsNot: new HashSet<string>(),
            requiredPrefix: new HashSet<string>(),
            yieldToSurface: new HashSet<string>()
        );

        var result = _serializer.Serialize(emptyData);

        Assert.Equal("", result);
    }

    [Fact]
    public void RoundtripWithDataPreservesAllFields()
    {
        var original = new VocabNoteMatchingRulesData(
            surfaceIsNot: new HashSet<string> { "surface1", "surface2" },
            prefixIsNot: new HashSet<string> { "prefix1" },
            suffixIsNot: new HashSet<string> { "suffix1", "suffix2", "suffix3" },
            requiredPrefix: new HashSet<string> { "req1" },
            yieldToSurface: new HashSet<string> { "yield1", "yield2" }
        );

        var serialized = _serializer.Serialize(original);
        var deserialized = _serializer.Deserialize(serialized);

        Assert.Equal(new HashSet<string> { "surface1", "surface2" }, deserialized.SurfaceIsNot);
        Assert.Equal(new HashSet<string> { "prefix1" }, deserialized.PrefixIsNot);
        Assert.Equal(new HashSet<string> { "suffix1", "suffix2", "suffix3" }, deserialized.SuffixIsNot);
        Assert.Equal(new HashSet<string> { "req1" }, deserialized.RequiredPrefix);
        Assert.Equal(new HashSet<string> { "yield1", "yield2" }, deserialized.YieldToSurface);
    }
}
