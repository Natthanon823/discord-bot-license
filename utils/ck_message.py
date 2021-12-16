import discord

class ck_message:

    def __init__(self):
        pass


    async def gensuccess(self, ctx, _license, _count, _time):
        await ctx.send(f"Generate license success check in your DMs. | {ctx.author.mention}")
        try:
            await ctx.author.send(f"""```

LICENSE TIME: {_time}h
LICENSE COUNT: {_count}

YOUR LICENSE:
{_license}

GUILD: {ctx.guild.name}
```""")
        except:
            await ctx.send(f"""
YOUR CLOSE DM (IF YOU NEED LICENSE IN DM PLEASE OPEN YOUR DM)

```

LICENSE TIME: {_time}h
LICENSE COUNT: {_count}

YOUR LICENSE:
{_license}

GUILD: {ctx.guild.name}
```""")


    async def licenseexpire(self, ctx, _license, _licenserole, _guildname):
        _embed = discord.Embed(title = f"LICENSE EXPIRE ({_license})", description = f"- you was removed role `{_licenserole}` from `{_guildname}`", colour = discord.Color.dark_orange())
        await ctx.send(embed=_embed)

    async def redeemsuccess(self, ctx, _license, _licensetime, _licenserole):
        _embed = discord.Embed(title = f"Success ({_license})", description = f" - you got role `<@&{_licenserole}>` for `{_licensetime}` hours.", colour = discord.Color.green())
        await ctx.send(embed=_embed)

    async def redeeminvaild(sefl, ctx):
        _embed = discord.Embed(title = "Invaild License", description = " - check your license is correct?", colour = discord.Color.red())
        await ctx.send(embed=_embed)

    async def redeemused(self, ctx):
        _embed = discord.Embed(title = "Used License", description = " - this license has been used.", colour = discord.Color.orange())
        await ctx.send(embed=_embed)

    async def redeemerror(self, ctx):
        _embed = discord.Embed(title = "ERROR!", description = " - please contact dev", colour = discord.Color.dark_red())
        await ctx.send(embed=_embed)

    async def _cooldown(self, ctx, err):
        _embed = discord.Embed(title = "Cooldown!", description = f" - please wait and try again in {err.retry_after:.2f}s.", colour = discord.Color.dark_gold())
        await ctx.send(embed=_embed)