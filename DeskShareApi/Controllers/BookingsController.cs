using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using DeskShareApi.Models;
using Microsoft.AspNetCore.Authorization;

namespace DeskShareApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [Authorize]
    public class BookingsController : ControllerBase
    {
        private readonly DbContextDeskShare _context;

        public BookingsController(DbContextDeskShare context)
        {
            _context = context;
        }

        // GET: api/Bookings
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Bookings>>> Get_Bookings(bool freetoday,bool freetomorrow,bool freeweek)
        {
            if (!freetoday&&!freetomorrow&&!freeweek)
            {
                return await _context._Bookings.Where(x=>x._End>DateTime.Now).OrderBy(x => x._End).ToListAsync();
            }

            //Gegenteil auswählen um eine Ebene tiefer Desks auszusortieren
            if (freetoday)
            {
             
                var rtn= await _context._Bookings.Where(x=> x._Start.DayOfYear <= DateTime.Now.DayOfYear && DateTime.Now.DayOfYear<= x._End.DayOfYear).OrderBy(x => x._End).ToListAsync();
                return rtn;

            }
            if (freetomorrow)
            {
                var rtn2 = await _context._Bookings.Where(x => x._Start.AddDays(1) <= DateTime.Now.AddDays(1) && x._End.AddDays(1) >= DateTime.Now.AddDays(1)).OrderBy(x => x._End).ToListAsync();
                return rtn2;
            }
            var rtn3 = await _context._Bookings.Where(x => x._Start <= DateTime.Now && x._End  >= DateTime.Now.AddDays(7)).OrderBy(x => x._End).ToListAsync();
            return rtn3;
        }

        // GET: api/Bookings/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Bookings>> GetBookings(int id)
        {
            var bookings = await _context._Bookings.FindAsync(id);

            if (bookings == null)
            {
                return NotFound();
            }

            return bookings;
        }

        // GET: api/Bookings/byUser?id=xxxxxx&status=true
        [HttpGet]
        [Route("byUser")]
        public async Task<ActionResult<IEnumerable<Bookings>>> GetBookingsByUser(string id)
        {
           
                var bookings = await _context._Bookings.Where(x => x._User.Equals(id) && x._End > DateTime.Now).ToListAsync() ;
            
            

            if (bookings == null)
            {
                return NotFound();
            }

            return Ok(bookings);
        }

        
        // GET: api/Bookings/byDesk?id=xxxxxx&status=true
        [HttpGet]
        [Route("byDesk")]
        public async Task<ActionResult<IEnumerable<Bookings>>> GetBookingsByDesk(int id,bool? status)
        {
           
           
                var bookings = await _context._Bookings.Where(x => x._Desk.Equals(id) && x._End > DateTime.Now).ToListAsync();
          
         

            if (bookings == null)
            {
                return NotFound();
            }

            return Ok(bookings);
        }

        // PUT: api/Bookings/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutBookings(int id, Bookings bookings)
        {
            if (id != bookings._Id)
            {
                return BadRequest();
            }

            _context.Entry(bookings).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!BookingsExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Bookings
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Bookings>> PostBookings(Bookings bookings)
        {
            _context._Bookings.Add(bookings);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetBookings", new { id = bookings._Id }, bookings);
        }

        // DELETE: api/Bookings/5?uid=""
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBookings(int id,string uid)
        {
            var bookings = await _context._Bookings.FindAsync(id);
            if (bookings == null)
            {
                return NotFound();
            }

            if (bookings._User!=uid)
            {
                return Unauthorized();
            }
            _context._Bookings.Remove(bookings);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool BookingsExists(int id)
        {
            return _context._Bookings.Any(e => e._Id == id);
        }
    }
}
