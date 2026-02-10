namespace JAStudio.Core.InteropExperiments;

public class CustomTypeReceiver
{
    public string ReceiveClass(dynamic instance) => instance.a_value;
}