from music_bot import *
from configuration import *

config_file = 'config.json'
configuration = read_configuration(config_file)
discord_token = configuration["discord_token"]
discord_guild_id = configuration["discord_guild_id"]
discord_command_prefix = "!"

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

if __name__ == "__main__":
    print(f'Discord token: {discord_token}')
    print(f'Discord guild: {discord_guild_id}')

    bot.run(discord_token)
    bot.finalize()