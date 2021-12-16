import config
import os
from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

print(f"Logging in...")

bot = Bot(command_prefix=".", intents=Intents.all())
slash = SlashCommand(bot, sync_commands=True)

print("")
print(f"Cogs loading....")
cogs_lsit = 0
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        cogs_lsit +=1
        print(f"[{cogs_lsit}] {name}")
        a = bot.load_extension(f"cogs.{name}")

bot.run(config._TOKEN)
