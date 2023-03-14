import pathlib
from MusicBot.music_bot import *
from Configuration.configuration import *
import asyncio
import platform

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

config_file = '{}/config.json'.format(pathlib.Path(__file__).parent.resolve())
configuration = read_configuration(config_file)
discord_token = configuration["discord_token"]
discord_guild_id = configuration["discord_guild_id"]
discord_command_prefix = "!"

if __name__ == "__main__":
    print(f'Discord token: {discord_token}')
    print(f'Discord guild: {discord_guild_id}')
    bot = MusicBot(discord_command_prefix, discord_guild_id)

    @bot.command(name='play')
    async def play(ctx, *, message):
        if ctx.guild.id != ctx.bot.guild_id:
            print(f'Skipping because guild_id({ctx.guild.id}) is different than {ctx.bot.guild_id}')
            return

        await ctx.send(f'Responding to message({message}) in guild with id: {ctx.guild.id}')

    @bot.event
    async def on_ready():
        print("Logged in as a bot {0.user}".format(bot))

    bot.run(discord_token)
    bot.finalize()