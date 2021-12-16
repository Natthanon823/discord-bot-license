from discord import Game
from discord.ext import commands



class ck_bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Game(name="#CHAKEAW LICENSE"))
        print("")
        print("----------------------------------------------")
        print("")
        print(f"Bot online: {self.bot.user}")
        print("")
        print("----------------------------------------------")
        print("")

def setup(bot):
    bot.add_cog(ck_bot(bot))