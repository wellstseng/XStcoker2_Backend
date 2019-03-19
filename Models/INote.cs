using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace XStcoker2_Backend.Models
{
    public interface INote
    {
        int Id { get; set; }
        string Title { get; set; }
        string Content { get; set; }
        string Author { get; set; }
    }
}
