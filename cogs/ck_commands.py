import discord
from discord.ext import commands
from discord.ext.commands import errors

from utils import ck_message

class ck_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sendMessage = ck_message.ck_message()


    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, err):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            return

        elif isinstance(err, errors.MissingRequiredArgument):
            pass

        elif isinstance(err, errors.NotOwner):
            pass

        elif isinstance(err, errors.BotMissingPermissions):
            pass

        elif isinstance(err, errors.RoleNotFound):
            pass

        elif isinstance(err, errors.UserNotFound):
            pass

        elif isinstance(err, errors.MissingPermissions):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await self.sendMessage._cooldown(ctx, err)

def setup(bot):
    bot.add_cog(ck_commands(bot))