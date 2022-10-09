import asyncio
import logging
import os

from discord import Intents, utils
from discord.ext import commands
from discord.ext.commands import ExtensionFailed
from replit import db
from scss import Compiler

from frontend import frontend


class Main:
    def __init__(self):
        log_handler = logging.StreamHandler()
        utils.setup_logging(handler=log_handler)
        self.logger = logging.getLogger("main")
        self.logger.info("Starting main class")

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
        self.logger.info("Bot Ready")
        if 'guilds' not in db.keys():
            db['guilds'] = {}
        for guild in self.bot.guilds:
            db['guilds'][guild.id] = {
                'name': guild.name,
                'channels': [ch.id for ch in guild.channels],
                'members': [mem.id for mem in guild.members]
            }

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
