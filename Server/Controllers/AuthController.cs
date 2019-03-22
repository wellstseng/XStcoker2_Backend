using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using XStcoker2_Backend.Data;
using XStcoker2_Backend.Models;

namespace XStcoker2_Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase {
        private readonly AuthenticationContext _context;

        public AuthController(AuthenticationContext context)
        {
            this._context = context;
        }

        // GET api/values
        //[HttpGet]
        //public ActionResult<IEnumerable<INote>> Get()
        //{
        //    return this._repository.GetList().ToList<INote>();
        //}

        // GET api/values/5
        //[HttpGet("{id}")]
        //public ActionResult<INote> Get(int id)
        //{
        //    return new  ActionResult<INote>(this._repository.GetNote(id));
        //}

        // POST api/values
        [HttpPost]
        public void Post([FromBody] string value)
        {
        }

        // PUT api/values/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] string value)
        {
        }

        // DELETE api/values/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }
    }
}
