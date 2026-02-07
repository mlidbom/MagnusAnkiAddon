using System;

namespace JAStudio.PythonInterop.Utilities;

public class PythonObjectWrapper(dynamic pythonObject)
{
   readonly dynamic _pythonObject = pythonObject;

   public TValue Use<TValue>(Func<dynamic, TValue> func) => PythonEnvironment.Use(() => func(_pythonObject));
   public void Use(Action<dynamic> func) => PythonEnvironment.Use(() => func(_pythonObject));
}
