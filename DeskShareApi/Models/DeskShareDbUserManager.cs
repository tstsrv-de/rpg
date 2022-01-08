using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace DeskShareApi.Models
{
    public class DeskShareDbUserManager : IdentityDbContext<UserIdentity>
    {
        public DeskShareDbUserManager(DbContextOptions<DeskShareDbUserManager> options) : base(options)
        {
        }
        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);
        }

    }
}
