using System.Collections.Generic;
using Compze.Utilities.Testing.Must;
using JAStudio.PythonInterop;
using JAStudio.PythonInterop.Utilities;
using Xunit;

namespace JAStudio.Core.Tests.Interop;

public class PythonDotNetShimTests
{
   [Fact] public void RoundTrippingStringListResultInIdenticalList()
   {
      List<string> expected = ["1", "2", "3"];
      List<string> other = (List<string>)PythonDotNetShim.StringList.ToDotNet(
         PythonDotNetShim.StringList.ToPython(expected));

      other.Must().DeepEqual(expected);

      //this is way too slow, we need another aproach for our amounts of data
      PythonEnvironment.Use(() =>
      {
         for(int i = 0; i < 10000; i++)
         {
            other = (List<string>)PythonDotNetShim.StringList.ToDotNet(PythonDotNetShim.StringList.ToPython(expected));
         }
      });
   }

   [Fact] public void RoundTrippingStringStringDictsResultInIdenticalDict()
   {
      Dictionary<string, string> expected = new Dictionary<string, string>
                                            {
                                               ["1"] = "2",
                                               ["3"] = "4"
                                            };
      var other = (Dictionary<string, string>)PythonDotNetShim.StringStringDict.ToDotNet(
         PythonDotNetShim.StringStringDict.ToPython(expected));

      other.Must().DeepEqual(expected);

      //this is way too slow, we need another aproach for our amounts of data
      PythonEnvironment.Use(() =>
      {
         for(int i = 0; i < 10000; i++)
         {
            other = (Dictionary<string, string>)PythonDotNetShim.StringStringDict.ToDotNet(PythonDotNetShim.StringStringDict.ToPython(expected));
         }
      });
   }
}
