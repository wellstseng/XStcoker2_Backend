using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace XStcoker2_Backend.Models
{
    public class Note:INote
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Content { get; set; }
        public string Author { get; set; }
    }
}
