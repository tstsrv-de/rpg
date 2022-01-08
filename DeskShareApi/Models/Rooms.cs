using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace DeskShareApi.Models
{
    [Table("rooms")]
    public class Rooms
    {
        [Column("ID")] [Key] [DatabaseGenerated(DatabaseGeneratedOption.Identity)] public int _Id { get; set; }
        [Column("FLOOR")] public int _FloorId { get; set; }
        [Column("NAME")] public string _Name { get; set; }
        [Column("ORDER")] public int _Order { get; set; }
    }
}
