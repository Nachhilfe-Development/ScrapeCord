from dotenv import load_dotenv
import os
import json
import discord
from discord.ext import commands

import sys
from pathlib import Path
sys.path.append(Path(".").resolve().as_posix())

from src.scraper import Scraper


bot = commands.Bot()


@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is ready!")


@bot.slash_command(name="print-output")
async def print_output(ctx: discord.ApplicationContext, limit: int = 10, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    await ctx.respond(f"Printing last {limit} messages from {channel.mention}", ephemeral=True)

    scraper = Scraper(channel, limit)
    data = await scraper.scrape_channel()
    print(json.dumps(data, indent=4, sort_keys=True))


if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv("bot-token"))
