using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.DependencyInjection;

namespace DeskShareApi.Models
{
    public class SeedDb
    {

        public static void Initialize(IServiceProvider serviceProvider)
        {
            var context = serviceProvider.GetRequiredService<DeskShareDbUserManager>();
            var userManager = serviceProvider.GetRequiredService<UserManager<UserIdentity>>();
            context.Database.EnsureCreated();
            if (!context.Users.Any())
            {
                var user1 = new UserIdentity()
                {
                    Email = "test@gmail.com",
                    UserName = "user",
                    _Perm = false,
                    SecurityStamp = Guid.NewGuid().ToString(),
                };
                var userRes = userManager.CreateAsync(user1, "Test@123").Result;

                var user2 = new UserIdentity()
                {
                    Email = "test2@gmail.com",
                    UserName = "adminuser",
                    _Perm = true,
                    SecurityStamp = Guid.NewGuid().ToString()
                };
                userManager.CreateAsync(user2, "Test@123");
            }

            context.SaveChanges();
            context.Dispose();

            var dataContext = serviceProvider.GetRequiredService<DbContextDeskShare>();
            dataContext.Database.EnsureCreated();

            if (!dataContext._Buildings.Any())
            {

                //seed buildings (3 buldings)
                #region buldings

                dataContext._Buildings.Add(new Buildings()
                {
                    _Order = 0,
                    _Location = "Hauptstraße 3",
                    _Name = "Ausbildungswerkstatt",
                });

                dataContext._Buildings.Add(new Buildings()
                {
                    _Order = 1,
                    _Location = "Hauptstraße 4",
                    _Name = "Verwaltung",
                });

                dataContext._Buildings.Add(new Buildings()
                {
                    _Order = 2,
                    _Location = "Hauptstraße 5",
                    _Name = "Werkstatt",
                });
                
                #endregion

                dataContext.SaveChanges();

                //seed floors (building 0 = 3 floors; bulding 1 = 5 floors; building 2 = 2 floors)
                var buildings = dataContext._Buildings.ToArray(); // 3 buildings
                #region floors

                //floors in building 0/2 (3 floors)
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 0,
                    _Name = "Erdgeschoss",
                    _BuildingId = buildings[0]._Id
                });
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 1,
                    _Name ="1 OG.",
                    _BuildingId = buildings[0]._Id
                });
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 2,
                    _Name ="2 OG.",
                    _BuildingId = buildings[0]._Id
                });

                //floors in building 1/2 (5 floors)
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 0,
                    _Name = "Erdgeschoss",
                    _BuildingId = buildings[1]._Id
                });
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 1,
                    _Name = "1 OG.",
                    _BuildingId = buildings[1]._Id
                });
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 2,
                    _Name = "2 OG.",
                    _BuildingId = buildings[1]._Id
                });
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 3,
                    _Name = "3 OG.",
                    _BuildingId = buildings[1]._Id
                });
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 4,
                    _Name = "4 OG.",
                    _BuildingId = buildings[1]._Id
                });

                //floors in building 2/2 (2 floors)
                dataContext._Floors.Add(new Floors()
                {
                    _Order = 0,
                    _Name = "Keller",
                    _BuildingId = buildings[2]._Id
                });

                dataContext._Floors.Add(new Floors()
                {
                    _Order = 1,
                    _Name = "Erdgeschoss",
                    _BuildingId = buildings[2]._Id
                });

               

                #endregion

                dataContext.SaveChanges();

                var floors = dataContext._Floors;
                var b0Floors = floors.Where(x => x._BuildingId.Equals(buildings[0]._Id)).ToArray(); // 3 floors
                var b1Floors = floors.Where(x => x._BuildingId.Equals(buildings[1]._Id)).ToArray(); // 5 floors
                var b2Floors = floors.Where(x => x._BuildingId.Equals(buildings[2]._Id)).ToArray(); // 2 floors

                //seed rooms (building 0 = 3 floors(5 rooms, 5 rooms, 2 rooms); bulding 1 = 5 floors (all 3 rooms); building 2 = 2 floors (3 rooms, 2 rooms))
                #region rooms

                #region building 0

                //rooms in building 0/2 - floor 0/2 (5 rooms)
                #region floor 0

                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Raum 11",
                    _FloorId = b0Floors[0]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Raum 12",
                    _FloorId = b0Floors[0]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 2,
                    _Name = "Raum 13",
                    _FloorId = b0Floors[0]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 3,
                    _Name = "Raum 14",
                    _FloorId = b0Floors[0]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 4,
                    _Name = "Raum 15",
                    _FloorId = b0Floors[0]._Id
                });
                #endregion

                //rooms in building 0/2 - floor 1/2 (5 rooms)
                #region floor 1

                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Raum 111",
                    _FloorId = b0Floors[1]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Raum 112",
                    _FloorId = b0Floors[1]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 2,
                    _Name = "Raum 113",
                    _FloorId = b0Floors[1]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 3,
                    _Name = "Raum 114",
                    _FloorId = b0Floors[1]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 4,
                    _Name = "Raum 115",
                    _FloorId = b0Floors[1]._Id
                });
                #endregion

                //rooms in building 0/2 - floor 2/2 (2 rooms)
                #region floor 2
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Raum 214",
                    _FloorId = b0Floors[2]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Raum 215",
                    _FloorId = b0Floors[2]._Id
                });
                #endregion

                #endregion

                #region building 1
                //rooms in building 1/2 - floor 0/4 (3 rooms)
                #region floor 0
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Raum 01",
                    _FloorId = b1Floors[0]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Raum 02",
                    _FloorId = b1Floors[0]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 2,
                    _Name = "Raum 03",
                    _FloorId = b1Floors[0]._Id
                });
                #endregion

                //rooms in building 1/2 - floor 1/4 (3 rooms)
                #region floor 1
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Raum 101",
                    _FloorId = b1Floors[1]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Raum 102",
                    _FloorId = b1Floors[1]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 2,
                    _Name = "Raum 103",
                    _FloorId = b1Floors[1]._Id
                });
                #endregion

                //rooms in building 1/2 - floor 2/4 (3 rooms)
                #region floor 2
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Raum 201",
                    _FloorId = b1Floors[2]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Raum 202",
                    _FloorId = b1Floors[2]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 2,
                    _Name = "Raum 203",
                    _FloorId = b1Floors[2]._Id
                });
                #endregion

                //rooms in building 1/2 - floor 3/4 (3 rooms)
                #region floor 3
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Raum 301",
                    _FloorId = b1Floors[3]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Raum 302",
                    _FloorId = b1Floors[3]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 2,
                    _Name = "Raum 303",
                    _FloorId = b1Floors[3]._Id
                });
                #endregion

                //rooms in building 1/2 - floor 4/4 (3 rooms)
                #region floor 4
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Raum 401",
                    _FloorId = b1Floors[4]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Raum 402",
                    _FloorId = b1Floors[4]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 2,
                    _Name = "Raum 403",
                    _FloorId = b1Floors[4]._Id
                });
                #endregion
                #endregion

                #region building 2
                //rooms in building 2/2 - floor 0/1 (3 rooms)
                #region floor 0
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Projektraum",
                    _FloorId = b2Floors[0]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Schulungsraum B1",
                    _FloorId = b2Floors[0]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 2,
                    _Name = "Schulungsraum B2",
                    _FloorId = b2Floors[0]._Id
                });
                #endregion

                //rooms in building 2/2 - floor 1/1 (2 rooms)
                #region floor 1
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 0,
                    _Name = "Schulungsraum C1",
                    _FloorId = b2Floors[1]._Id
                });
                dataContext._Rooms.Add(new Rooms()
                {
                    _Order = 1,
                    _Name = "Schulungsraum C2",
                    _FloorId = b2Floors[1]._Id
                });
                #endregion

                #endregion

                #endregion

                dataContext.SaveChanges();

                var rooms = dataContext._Rooms;
                var b0f0Rooms = rooms.Where(x => x._FloorId.Equals(b0Floors[0]._Id)).ToArray();// 5 rooms on floor 0 in building 0
                var b0f1Rooms = rooms.Where(x => x._FloorId.Equals(b0Floors[1]._Id)).ToArray();// 5 rooms on floor 1 in building 0
                var b0f2Rooms = rooms.Where(x => x._FloorId.Equals(b0Floors[2]._Id)).ToArray();// 2 rooms on floor 2 in building 0

                var b1f0Rooms = rooms.Where(x => x._FloorId.Equals(b1Floors[0]._Id)).ToArray();// 3 rooms on floor 0 in building 0
                var b1f1Rooms = rooms.Where(x => x._FloorId.Equals(b1Floors[1]._Id)).ToArray();// 3 rooms on floor 1 in building 0
                var b1f2Rooms = rooms.Where(x => x._FloorId.Equals(b1Floors[2]._Id)).ToArray();// 3 rooms on floor 2 in building 0
                var b1f3Rooms = rooms.Where(x => x._FloorId.Equals(b1Floors[3]._Id)).ToArray();// 3 rooms on floor 3 in building 0
                var b1f4Rooms = rooms.Where(x => x._FloorId.Equals(b1Floors[4]._Id)).ToArray();// 3 rooms on floor 4 in building 0

                var b2f0Rooms = rooms.Where(x => x._FloorId.Equals(b2Floors[0]._Id)).ToArray();// 3 rooms on floor 0 in building 0
                var b2f1Rooms = rooms.Where(x => x._FloorId.Equals(b2Floors[1]._Id)).ToArray();// 2 rooms on floor 1 in building 0

                //seed desks ()

                #region desks

                #region building 0

                #region floor 0 //5 rooms

                // 2 Desks
                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f0Rooms[0]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b0f0Rooms[0]._Id,
                    
                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });

                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f0Rooms[1]._Id,
                    
                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion
                #region room 2
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f0Rooms[2]._Id,
                    
                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b0f0Rooms[2]._Id,
                    
                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });

                #endregion
                #region room 3
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f0Rooms[3]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion
                #region room 4
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f0Rooms[4]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion

                #endregion

                #region floor 1 //5 rooms

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f1Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b0f1Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order =2,
                    _Name = "Tisch 3",
                    _RoomId = b0f1Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f1Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion
                #region room 2
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f1Rooms[2]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion
                #region room 3
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f1Rooms[3]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b0f1Rooms[3]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion
                #region room 4
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f1Rooms[4]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b0f1Rooms[4]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = false
                });
                #endregion

                #endregion

                #region floor 2 //2 rooms

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f2Rooms[0]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 3 ,
                    _Stand = true
                });
                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b0f2Rooms[1]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 3,
                    _Stand = true
                });
                #endregion

                #endregion

                #endregion

                #region building 1

                #region floor 0 //3 rooms

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f0Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = true
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f0Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = true
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 2,
                    _Name = "Tisch 3",
                    _RoomId = b1f0Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = true
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 3,
                    _Name = "Tisch 4",
                    _RoomId = b1f0Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = true
                });
                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f0Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f0Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion
                #region room 2
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f0Rooms[2]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f0Rooms[2]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion

                #endregion

                #region floor 1 //3 rooms

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f1Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f1Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f1Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f1Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion
                #region room 2
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f1Rooms[2]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f1Rooms[2]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion

                #endregion

                #region floor 2 //3 rooms

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f2Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f2Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f2Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f2Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion
                #region room 2
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f2Rooms[2]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f2Rooms[2]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = false,
                    _Mouse = false,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion

                #endregion

                #region floor 3 //3 rooms

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f3Rooms[0]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = true
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f3Rooms[0]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = true
                });
                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f3Rooms[1]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = true
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f3Rooms[1]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = true
                });
                #endregion
                #region room 2
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f3Rooms[2]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = true
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b1f3Rooms[2]._Id,

                    _Computer = true,
                    _Docking = false,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = true
                });
                #endregion

                #endregion

                #region floor 4 //3 rooms

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f4Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f4Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion
                #region room 2
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b1f4Rooms[2]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 1,
                    _Stand = false
                });
                #endregion

                #endregion

                #endregion

                #region building 2

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b2f0Rooms[0]._Id,

                    _Computer = true,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = true
                });
                #endregion

                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b2f0Rooms[1]._Id,

                    _Computer = true,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = true
                });
                #endregion
                #region room 2
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b2f0Rooms[2]._Id,

                    _Computer = true,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 2,
                    _Stand = true
                });
                #endregion

                #region floor 0 //3 rooms

                #endregion

                #region floor 1 //2 rooms

                #region room 0
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b2f1Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b2f1Rooms[0]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion
                #region room 1
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 0,
                    _Name = "Tisch 1",
                    _RoomId = b2f1Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = false
                });
                dataContext._Desks.Add(new Desks()
                {
                    _Order = 1,
                    _Name = "Tisch 2",
                    _RoomId = b2f1Rooms[1]._Id,

                    _Computer = false,
                    _Docking = true,
                    _Keyboard = true,
                    _Mouse = true,
                    _Screens = 4,
                    _Stand = false
                });
                #endregion

                #endregion

                #endregion

                #endregion
                dataContext.SaveChanges();
            }

        }
    }
}
