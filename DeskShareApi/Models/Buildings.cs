using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace DeskShareApi.Models
{
    [Table("buildings")]
    public class Buildings
    {
        [Column("ID")] [Key] [DatabaseGenerated(DatabaseGeneratedOption.Identity)] public int _Id { get; set; }

        [Column("ORDER")] public int _Order { get; set; }
        [Column("LOCATION")] public string _Location { get; set; } 
        [Column("NAME")] public string _Name { get; set; }
    }
}
