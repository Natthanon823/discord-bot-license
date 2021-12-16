from os import name
import string
import discord

from decimal import *
from random import choice
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

import config
from utils import ck_db, ck_time
from utils import ck_message

class ck_license(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._ckTemp3 = {}
        self.sendMessage = ck_message.ck_message()
        self.check_license.start()


    def _genCode(self, x):
        return ''.join(choice(string.digits + string.ascii_letters) for _ in range(x))

    def replaceLicense(self, _license):
        return str(_license).replace("'", "").replace("]", "").replace(" ", "").replace("[", " ").replace(",", "\n ")

    async def remove_role(self, guild_id, member_id, role_id):
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(int(member_id))
        role = guild.get_role(int(role_id))
        await member.remove_roles(role)
        return member, role, guild

    async def add_role(self, guild_id, member_id, role_id):
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(int(member_id))
        role = guild.get_role(int(role_id))
        await member.add_roles(role)

    @tasks.loop(seconds = 60)
    async def check_license(self):
        for guild in self.bot.guilds:
            a = ck_db._checkLicenseActive(str(guild.id))
            if a[0] == "EXPIRE":
                _req = await self.remove_role(guild.id, a[2], a[3])
                await self.sendMessage.licenseexpire(_req[0], a[4], _req[1], _req[2])
                pass

    @cog_ext.cog_slash(name="generate",
        description="generate license (/generate roletag licensetime(1d, 1w, 1m, 1y) licensecount)",
        options=[
            create_option(
                name="role",
                description="Select the role want to create a license key. (tag role)",
                option_type=discord.Role,
                required=True,
            ),
            create_option(
                name="time",
                description="Enter the duration of license key you want. (Ex. 1m or 1w)",
                option_type=str,
                required=True,
            ),
            create_option(
                name="count",
                description="Enter the number of license key you want. (not more than 25)",
                option_type=int,
                required=True
            )
        ]
    )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def genlicense(self, ctx, role: discord.Role, time: str, count: int):
        if count > 25:
            await ctx.send("limit 25 license key")
            return
        self._ckTemp3.update({ctx.author.id: {"data": []}})
        for i in range(int(count)):
            _ckTemp2 = {
                "_guildID": str(ctx.guild_id),
                "license": str(f"{self._genCode(5)}-{self._genCode(5)}-{self._genCode(5)}-{self._genCode(5)}-{self._genCode(5)}"),
                "licenseTIME": ck_time.time_string_to_hours(str(time)),
                "addID": str(ctx.author.id),
                "roleID": str(role.id),
            }
            self._ckTemp3[ctx.author.id]["data"].append(_ckTemp2["license"])
            ck_db._addLicense(_guildID = _ckTemp2["_guildID"], get_license = _ckTemp2["license"], get_licenseTIME = _ckTemp2["licenseTIME"], get_roleID = _ckTemp2["roleID"], get_addid = _ckTemp2["addID"])
        await self.sendMessage.gensuccess(ctx, self.replaceLicense(self._ckTemp3[ctx.author.id]["data"]), count, _ckTemp2["licenseTIME"])


    @cog_ext.cog_slash(name="redeem", 
    description="generate license (/redeem <license key>)",
    options=[
        create_option(
            name="license",
            description="Enter your license key",
            option_type=str,
            required=True,
        ),
    ]
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def redeemlicense(self, ctx: SlashContext, license: str):
        a = ck_db._redeemLicense(_guildID = str(ctx.guild.id), get_license = str(license), get_redeemid = str(ctx.author.id))
        print(a)
        if a[0] == "SUCCESS":
            await self.add_role(ctx.guild.id, ctx.author.id, a[2])
            await self.sendMessage.redeemsuccess(ctx, license, a[1], a[2])
        elif a[0] == "INVAILD":
            await self.sendMessage.redeeminvaild(ctx)
        elif a[0] == "USED":
            await self.sendMessage.redeemused(ctx)
        else:
            await self.sendMessage.redeemerror(ctx)

    @cog_ext.cog_slash(name="delete", description="delete license (/delete <license key>)")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def deletelicense(self, ctx: SlashContext, arg1: int and str):
        a = ck_db._removeLicense(_guildID = str(ctx.guild.id), get_license = str(arg1))
        await ctx.send(a)

def setup(bot):
    bot.add_cog(ck_license(bot))
