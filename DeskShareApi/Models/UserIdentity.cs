using Microsoft.AspNetCore.Identity;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace DeskShareApi.Models
{


    [Table("aspnetusers")]
    public class UserIdentity : IdentityUser
    {
        public bool _Perm { get; set; }
    }
}
