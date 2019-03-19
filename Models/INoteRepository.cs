using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace XStcoker2_Backend.Models
{
    public interface INoteRepository
    {
        INote GetNote(int id);
        IEnumerable<INote> GetList();
    }
}
