import re
import discord
from discord.ext import commands
from dice import summarize

class DiceCommands(commands.Cog, name="Dice Commands"):
  "These are commands for rolling dice"

  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    name="roll",
    aliases = ["r"]
  )
  async def roll(self, ctx, msg: str, member: discord.Member=None):
    msg_re = re.compile(r'([0-9])d([0-9]{1,2})(\+([0-9])d([0-9]{1,2}))?([+-][0-9])?$')
    dice_match = msg_re.match(msg)
    dice = []
    if dice_match is not None:
      groups = dice_match.groups()
      dice_1 = (groups[0], groups[1])
      dice.append(dice_1)
      if groups[2] is not None:
        dice_2 = (groups[3], groups[4])
        dice.append(dice_2)
      mod = groups[5]
      result = summarize(dice, mod)
      await ctx.send(f'`{result}`')
      
  
def setup(bot):
  bot.add_cog(DiceCommands(bot))
