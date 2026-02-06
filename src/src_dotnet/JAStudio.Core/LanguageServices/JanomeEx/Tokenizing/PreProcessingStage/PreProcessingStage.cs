using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;

public class PreProcessingStage
{
    private readonly VocabCollection _vocabs;

    public PreProcessingStage(VocabCollection vocabs) => _vocabs = vocabs;

    public List<IAnalysisToken> PreProcess(List<JNToken> tokens) => tokens.SelectMany(PreProcessToken).ToList();

    private List<IAnalysisToken> PreProcessToken(JNToken token)
    {
        // Note: The order here matters, it's not random. Any change will break things even should the tests be incomplete and not show it.
        
        if (token.Surface == JNToken.SplitterTokenText)
        {
            return [];
        }

        var splitGodanImperative = GodanImperativeSplitter.TrySplit(token);
        if (splitGodanImperative != null)
        {
            return splitGodanImperative;
        }

        var splitHybrid = IchidanGodanPotentialOrImperativeHybridSplitter.TrySplit(token, _vocabs);
        if (splitHybrid != null)
        {
            return splitHybrid;
        }

        var splitIchidanImperative = IchidanImperativeSplitter.TrySplit(token);
        if (splitIchidanImperative != null)
        {
            return splitIchidanImperative;
        }

        var splitDictionaryFormVerb = DictionaryFormVerbSplitter.TrySplit(token);
        if (splitDictionaryFormVerb != null)
        {
            return splitDictionaryFormVerb;
        }

        return [token];
    }
}
