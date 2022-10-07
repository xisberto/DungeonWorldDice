import asyncio
import os

from discord import Intents
from discord.ext import commands
from discord.ext.commands import ExtensionFailed
from scss import Compiler

from frontend import frontend


class Main:
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(
            command_prefix=".",
            intents=intents
        )
        self.bot.author_id = os.environ['AUTHOR_ID']
        extensions = [
            'cogs.cog_chars'
        ]
        for ext in extensions:
            asyncio.run(self.load_extensions(ext))

    def run(self):
        token = os.environ.get("DISCORD_BOT_SECRET")
        self.bot.run(token)

    @commands.Cog.listener()
    async def on_ready(self):
        print("I'm in")

    async def load_extensions(self, extension):
        try:
            await self.bot.load_extension(extension)
        except ExtensionFailed as ef:
            print(ef)


def compile_scss():
    source = 'static/css/main.scss'
    destination = open('static/css/main.css', 'w')
    destination.write(Compiler(output_style='compressed').compile(source))


if __name__ == '__main__':
    compile_scss()
    main = Main()
    frontend()
    main.run()
