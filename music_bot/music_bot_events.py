from discord.ext import commands

class MusicBotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as a bot {0.user}".format(self.bot))

    @commands.Cog.listener()
    async def on_disconnect_client(self, voice_client):
        if voice_client is None:
            print('Bot is not added to guild')
            return None
    
        if not voice_client.is_connected():
            print('Bot is not connected to any channel')
            return None
        
        await voice_client.disconnect()