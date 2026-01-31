namespace JAStudio.Core.Ports;

using System.Collections.Generic;
using Domain;

public interface IJapaneseNlpProvider
{
    List<Token> Tokenize(string text);
}
