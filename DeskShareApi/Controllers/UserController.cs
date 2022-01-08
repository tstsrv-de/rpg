using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using DeskShareApi.Models;
using Microsoft.AspNetCore.Identity;
using System.Security.Claims;
using System.IdentityModel.Tokens.Jwt;
using Microsoft.IdentityModel.Tokens;
using System.Text;

namespace DeskShareApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly UserManager<UserIdentity> _userManager;

        public UserController(UserManager<UserIdentity> userManager)
        {
            _userManager = userManager;
        }

        [HttpGet]
        [Route("perm")]
        public async Task<IActionResult> GetPermStatus(string uid)
        {
            var user = await _userManager.FindByIdAsync(uid);
            if (user._Perm)
            {
                return Ok();
            }

            return Unauthorized();
        }

        [HttpPost]
        [Route("login")]
        public async Task<IActionResult> Login([FromBody] LoginModel model)
        {
            var user = await _userManager.FindByNameAsync(model.Username);
            if (user == null || !await _userManager.CheckPasswordAsync(user, model.Password)) return Unauthorized();

            var authClaims = CreateClaim(model);
            var authSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("Bf]R86kM+buEB3'K"));
            var token = CreateToken(authClaims, authSigningKey);

            return Ok(new
            {
                user=user.Id,
                token = new JwtSecurityTokenHandler().WriteToken(token),
                expiration = token.ValidTo
            });
        }

        private static JwtSecurityToken CreateToken(IEnumerable<Claim> authClaims,SecurityKey authSigningKey)
        {
            return new JwtSecurityToken(
                issuer: "https://localhost",
                audience: "https://localhost",
                expires: DateTime.Now.AddDays(5),
                claims: authClaims,
                signingCredentials: new SigningCredentials(authSigningKey, SecurityAlgorithms.HmacSha256)
            );
        }

        private static IEnumerable<Claim> CreateClaim(LoginModel model)
        {
            return new[]
            {
                new Claim(JwtRegisteredClaimNames.Sub, model.Username),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
            };
        }

    }
}
