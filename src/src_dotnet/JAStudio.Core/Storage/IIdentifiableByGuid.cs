using System;

namespace JAStudio.Core.Storage;

public interface IIdentifiableByGuid
{
   Guid Id { get; }
}
