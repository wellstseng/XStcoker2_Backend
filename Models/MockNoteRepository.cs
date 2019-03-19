using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace XStcoker2_Backend.Models
{
    public class MockNoteRepository:INoteRepository
    {
        private readonly List<INote> _noteList = new List<INote>()
        {
            new Note() {Id=1, Author="Mary", Title="Title Mary", Content="Hello!"},
            new Note() {Id=2, Author="John", Title="Title John", Content="Hello  HI!"},
            new Note() {Id=3, Author="Mark", Title="Title Mark", Content="Note 1!"},
            new Note() {Id=4, Author="Teddy", Title="Title Teddy", Content="How are you!"}
        }; 
         
        public INote GetNote(int id)
        {
            return this._noteList.FirstOrDefault<INote>(note => note.Id == id);
        }

        public IEnumerable<INote> GetList()
        {
            return this._noteList;
        }

    }
}
