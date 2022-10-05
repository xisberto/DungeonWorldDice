import os

from discord import Intents
from discord.ext import commands

from frontend import frontend

intents = Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(
    command_prefix=".",
    intents=intents
)

bot.author_id = os.environ['AUTHOR_ID']


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
    'cogs.cog_example',
    'cogs.cog_chars'
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

frontend()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
