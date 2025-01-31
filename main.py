import os
import asyncio
import platform
from music_bot.music_bot import *
from music_bot.music_bot_commands import *
from music_bot.music_bot_events import *

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

DISCORD_TOKEN = os.environ.get("DiscordToken", None)
DISCORD_GUID_ID = os.environ.get("DiscordGuildId", None)
DISCORD_COMMAND_PREFIX = "!"

if __name__ == "__main__":
    print(f'Discord token: {DISCORD_TOKEN}')
    print(f'Discord guild: {DISCORD_GUID_ID}')
    bot = MusicBot(DISCORD_COMMAND_PREFIX, DISCORD_GUID_ID)

    asyncio.run(bot.add_cog(MusicBotCommands(bot)))
    asyncio.run(bot.add_cog(MusicBotEvents(bot)))
    
    bot.run(DISCORD_TOKEN)