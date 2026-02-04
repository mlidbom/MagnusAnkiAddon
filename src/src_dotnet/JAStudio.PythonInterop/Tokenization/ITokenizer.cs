using System.Collections.Generic;

namespace JAStudio.PythonInterop.Tokenization;

public interface ITokenizer
{
    List<Token> Tokenize(string text);
}
