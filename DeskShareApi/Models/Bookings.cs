using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace DeskShareApi.Models
{
    [Table("bookings")]
 
    public class Bookings
    {
        [Column("ID")] [Key] [DatabaseGenerated(DatabaseGeneratedOption.Identity)] public int _Id { get; set; }
        [Column("START")] public DateTime _Start { get; set; }
        [Column("END")] public DateTime _End { get; set; }
        [Column("TIMESTAMP")] public DateTime _Timestamp { get; set; }

        [Column("USER")] public string _User { get; set; }
        [Column("DESK")] public int _Desk { get; set; }
    }
}
