from discord.ext import commands

class MusicBot(commands.Bot):

    def __init__(self, prefix, guild_id):
        super().__init__(command_prefix=prefix)
        self.guild_id = int(guild_id)

    def finalize(self):
        print("closing bot")