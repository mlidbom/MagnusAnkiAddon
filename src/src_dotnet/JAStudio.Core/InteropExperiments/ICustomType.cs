using System;

namespace JAStudio.Core.InteropExperiments;



public class CustomTypeReceiver
{
    public string ReceiveClass(dynamic value) => value.AValue;
}