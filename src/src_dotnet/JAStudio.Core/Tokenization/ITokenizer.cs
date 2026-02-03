using System.Collections.Generic;

namespace JAStudio.Core.Tokenization;

public interface ITokenizer
{
    List<Token> Tokenize(string text);
}
