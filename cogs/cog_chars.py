import discord
from discord.ext import commands
import chars

class CharCommands(commands.Cog, name="Char Commands"):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command("save")
  async def save(self, ctx, attr, *value, member: discord.Member = None):
    if attr not in chars.attrs:
      await ctx.send("Invalid attribute")
      return
    char_id = self.get_id(ctx)
    char = chars.load(char_id)
    char[attr] = value
    chars.save(char)
    await ctx.send(embed=self.embed(char))

  @commands.command("whoami")
  async def whoami(self, ctx, *, member: discord.Member = None):
    char_id = self.get_id(ctx)
    char = chars.load(char_id)
    await ctx.send(embed=self.embed(char))

  @commands.command("forget")
  async def forget(self, ctx, *, member: discord.Member = None):
    chars.delete(self.get_id(ctx))
    await ctx.send("Forgot about your character")

  def get_id(self, ctx):
    return f'{ctx.guild.id}_{ctx.author.id}'

  def embed(self, char):
    char_name = " "
    print(type(char['name']))
    if type(char['name']) == str:
      char_name = char['name']
    else:
      char_name = " ".join(char['name'])
    print(char_name)
    response = discord.Embed(title=char_name, color=discord.Color.red())
    for attr in char.keys():
      if attr == 'name' or attr == 'player':
        continue
      response.add_field(name=attr, value=char[attr], inline=True)
    return response


def setup(bot):
  bot.add_cog(CharCommands(bot))
