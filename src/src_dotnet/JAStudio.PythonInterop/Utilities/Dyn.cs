using System.Collections.Generic;

namespace JAStudio.PythonInterop.Utilities;

public static class Dyn
{
    public static IEnumerable<dynamic> Enumerate(dynamic obj)
    {
        foreach (var item in obj)
        {
            yield return item;
        }
    }
}