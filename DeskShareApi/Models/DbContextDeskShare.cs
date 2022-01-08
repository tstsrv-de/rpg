using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace DeskShareApi.Models
{
    public class DbContextDeskShare : DbContext
    {
        public DbContextDeskShare(DbContextOptions<DbContextDeskShare> options) : base(options)
        {
           
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
        }

        
       public DbSet<Bookings> _Bookings { get; set; }
       public DbSet<Desks> _Desks { get; set; }
       public DbSet<Rooms> _Rooms { get; set; }
       public DbSet<Floors> _Floors { get; set; }
       public DbSet<Buildings> _Buildings { get; set; }
       public DbSet<UserIdentity> _User { get; set; }

    }
}
