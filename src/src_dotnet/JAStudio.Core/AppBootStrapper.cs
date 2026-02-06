using System;

namespace JAStudio.Core;
using SimpleInjector;

static class AppBootStrapper
{
   public static App Bootstrap()
   {
      var container = new Container();
      //register all the currently static class as singletons unsing factory method registrations, not the magic autodetect and wire together registration style.
      //We want manual constructor calls so we can use find usages etc and see how our code works
      throw new NotImplementedException();
   }
}
