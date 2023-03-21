import pathlib
import asyncio
import platform
from music_bot.music_bot import *
from music_bot.music_bot_commands import *
from music_bot.music_bot_events import *
from configuration.configuration import *

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

CONFIG_FILE = '{}/config.json'.format(pathlib.Path(__file__).parent.resolve())
CONFIGURATION = read_configuration(CONFIG_FILE)
DISCORD_TOKEN = CONFIGURATION["discord_token"]
DISCORD_GUID_ID = CONFIGURATION["discord_guild_id"]
DISCORD_COMMAND_PREFIX = "!"

if __name__ == "__main__":
    print(f'Discord token: {DISCORD_TOKEN}')
    print(f'Discord guild: {DISCORD_GUID_ID}')
    bot = MusicBot(DISCORD_COMMAND_PREFIX, DISCORD_GUID_ID)

    asyncio.run(bot.add_cog(MusicBotCommands(bot)))
    asyncio.run(bot.add_cog(MusicBotEvents(bot)))
    
    bot.run(DISCORD_TOKEN)