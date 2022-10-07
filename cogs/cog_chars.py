import re

import discord
from discord.ext import commands

import chars
import dice


class CharCommands(commands.Cog, name="Char Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("save")
    async def save(self, ctx, attr, value, member: discord.Member = None):
        if attr not in chars.attrs:
            await ctx.send("Invalid attribute")
            return
        char_id = self.get_id(ctx)
        char = chars.load(char_id)
        char[attr] = f"{value}"
        chars.save(char)
        await ctx.send(embed=self.embed_char(char))

    @commands.command("me")
    async def whoami(self, ctx, *, member: discord.Member = None):
        char_id = self.get_id(ctx)
        print(f"Got whoami for {char_id}")
        char = chars.load(char_id)
        await ctx.send(embed=self.embed_char(char))

    @commands.command("forget")
    async def forget(self, ctx, *, member: discord.Member = None):
        chars.delete(self.get_id(ctx))
        await ctx.send("Forgot about your character")

    @commands.command(
        name="roll",
        aliases=["r"]
    )
    async def roll(self, ctx, msg: str, member: discord.Member = None):
        msg_re = re.compile(r'([0-9])d([0-9]{1,2})(\+([0-9])d([0-9]{1,2}))?([+-][0-9])?$')
        dice_match = msg_re.match(msg)

        attrs_re = re.compile(r'\+?([a-z]{3})')
        attrs_match = attrs_re.match(msg)

        dice_roll = []
        if dice_match is not None:
            # Roll XdY+Z dices
            groups = dice_match.groups()
            dice_1 = (groups[0], groups[1])
            dice_roll.append(dice_1)
            if groups[2] is not None:
                dice_2 = (groups[3], groups[4])
                dice_roll.append(dice_2)
            mod = groups[5]
            result = dice.summarize(dice_roll, mod)
            embed = self.embed_result(msg, result)
            await ctx.send(embed=embed)
        elif attrs_match is not None:
            # Roll based on characters attributes
            attr = attrs_match.groups()[0]
            char = chars.load(self.get_id(ctx))
            dice_roll = [(2, 6)]
            result = dice.summarize([(2, 6)], char[attr])
            embed = self.embed_result(f"{char['name']} +{attr}", result)
            await ctx.send(embed=embed)
        else:
            print("Nothing")

    def get_id(self, ctx):
        return f'{ctx.guild.id}_{ctx.author.id}'

    def embed_char(self, char):
        char_name = " "
        if type(char['name']) == str:
            char_name = char['name']
        else:
            char_name = " ".join(char['name'])
        response = discord.Embed(title=char_name, color=discord.Color.red())
        for attr, value in char.items():
            if attr == 'name' or attr == 'player':
                continue
            response.add_field(name=attr, value=value, inline=True)
        return response

    def embed_result(self, title, result):
        print(type(title))
        if type(title) != str:
            print("converting to str")
            title = " ".join(title)
        response = discord.Embed(title=title, color=discord.Color.red())
        response.description = result
        return response


async def setup(bot):
    await bot.add_cog(CharCommands(bot))
