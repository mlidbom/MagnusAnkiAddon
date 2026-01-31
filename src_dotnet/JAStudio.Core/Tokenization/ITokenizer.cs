using System.Collections.Generic;
using JAStudio.Core.Domain;

namespace JAStudio.Core.Tokenization;

public interface ITokenizer
{
    List<Token> Tokenize(string text);
}
