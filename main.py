import asyncio
import logging
import os

from discord import Intents, utils
from discord.ext import commands
from replit import db
from scss import Compiler

from frontend import frontend


class Main(commands.Bot):
    def __init__(self, command_prefix, intents: Intents):
        super().__init__(command_prefix, intents=intents)

        log_handler = logging.StreamHandler()
        utils.setup_logging(handler=log_handler)
        self.logger = logging.getLogger("main")
        self.logger.info("Starting main class")

        self.author_id = os.environ['AUTHOR_ID']
        extensions = [
            'cogs.cog_chars'
        ]
        for ext in extensions:
            asyncio.run(self.load_extension(ext))

    def run_bot(self):
        token = os.environ.get("DISCORD_BOT_SECRET")
        self.run(token)

    async def on_ready(self):
        self.logger.info("Bot Ready")
        if 'guilds' not in db.keys():
            db['guilds'] = {}
        for guild in self.guilds:
            db['guilds'][guild.id] = {
                'name': guild.name,
                'channels': [ch.id for ch in guild.channels],
                'members': [mem.id for mem in guild.members]
            }
        self.logger.info(f"Bot is member of {len(db['guilds'])} guilds")


def compile_scss():
    source = 'static/css/main.scss'
    destination = open('static/css/main.css', 'w')
    destination.write(Compiler(output_style='compressed').compile(source))


if __name__ == '__main__':
    compile_scss()
    ints = Intents.default()
    ints.message_content = True
    main = Main(command_prefix=".", intents=ints)
    frontend()
    main.run_bot()
