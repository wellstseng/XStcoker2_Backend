using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using XStcoker2_Backend.Models;

namespace XStcoker2_Backend.Data
{
    public class AuthenticationContext : IdentityDbContext
    {
        public AuthenticationContext(DbContextOptions<AuthenticationContext> options) : base(options) { }
        public DbSet<ApplicationUser> ApplicationUsers { get; set; }
    }
}
