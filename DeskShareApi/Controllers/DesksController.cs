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
    public class DesksController : ControllerBase
    {
        private readonly DbContextDeskShare _context;

        public DesksController(DbContextDeskShare context)
        {
            _context = context;
        }

        // GET: api/Desks
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Desks>>> Get_Desks(bool mouse, bool keyboard, bool computer, bool docking, bool noscreen, bool onescreen, bool twoscreens, bool threescreens)
        {
            if (!mouse&&!keyboard&&!computer&&!docking&&!noscreen&&!onescreen&&!twoscreens&&!threescreens)
            {
                return await _context._Desks.OrderBy(x => x._Order).ToListAsync();
            }

            var screenCount = 0;
            if(onescreen) screenCount = 1;
            if(twoscreens) screenCount = 2;
            if(threescreens) screenCount = 3;
            return await _context._Desks.Where(x=>x._Mouse.Equals(mouse)||x._Keyboard.Equals(keyboard) || x._Computer.Equals(computer) || x._Docking.Equals(docking) || x._Screens>= screenCount).OrderBy(x => x._Order).ToListAsync();
        }

        // GET: api/Desks/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Desks>> GetDesks(int id)
        {
            var desks = await _context._Desks.FindAsync(id);

            if (desks == null)
            {
                return NotFound();
            }

            return desks;
        }

        [HttpGet]
        [Route("byRoom")]
        public async Task<ActionResult<Desks>> GetDesksByRoom(int id)
        {
            var desks = await _context._Desks.Where(x=>x._RoomId.Equals(id)).ToListAsync();

            if (desks == null)
            {
                return NotFound();
            }

            return Ok(desks);
        }

        // PUT: api/Desks/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutDesks(int id, Desks desks)
        {
            if (id != desks._Id)
            {
                return BadRequest();
            }

            _context.Entry(desks).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!DesksExists(id))
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

        // POST: api/Desks
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Desks>> PostDesks(Desks desks)
        {
            _context._Desks.Add(desks);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetDesks", new { id = desks._Id }, desks);
        }

        // DELETE: api/Desks/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteDesks(int id)
        {
            var desks = await _context._Desks.FindAsync(id);
            if (desks == null)
            {
                return NotFound();
            }

            _context._Desks.Remove(desks);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool DesksExists(int id)
        {
            return _context._Desks.Any(e => e._Id == id);
        }
    }
}
