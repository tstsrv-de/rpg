using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace DeskShareApi.Models
{
    [Table("desks")]
    public class Desks
    {
        [Column("ID")] [Key] [DatabaseGenerated(DatabaseGeneratedOption.Identity)] public int _Id { get; set; }
        [Column("ROOM")] public int _RoomId { get; set; }
        [Column("NAME")] public string _Name { get; set; }
        [Column("ORDER")] public int _Order { get; set; }
        [Column("SCREENS")] public int _Screens { get; set; }
        [Column("KEYBOARD")] public bool _Keyboard { get; set; }
        [Column("MOUSE")] public bool _Mouse { get; set; }
        [Column("DOCKING")] public bool _Docking { get; set; }
        [Column("COMPUTER")] public bool _Computer { get; set; }
        [Column("STAND")] public bool _Stand { get; set; }
      

    }
}
