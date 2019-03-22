using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using XStcoker2_Backend.Models;

namespace XStcoker2_Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ApplicationUserController : ControllerBase
    {
        private UserManager<ApplicationUser> _userManager;
        private SignInManager<ApplicationUser> _signinManager;
        public ApplicationUserController(UserManager<ApplicationUser> userManager, SignInManager<ApplicationUser> signinManager)
        {
            this._userManager = userManager;
            this._signinManager = signinManager;
        }

        [HttpPost]
        [Route("register")]
        public async Task<Object> PostRegisterApplicationUser(ApplicationUserModel model)
        {
            var applicationUser = new ApplicationUser()
            {
                UserName = model.UserName,
                Email = model.Email,
                FullName = model.FullName
            };

            try
            {
                var result = await this._userManager.CreateAsync(applicationUser, model.Password);
                return this.Ok(result);
            }
            catch(Exception ex) {
                throw ex;
            }
        }
    }
}