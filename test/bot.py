from dotenv import load_dotenv
import os
import json
import discord
from discord.ext import commands

import src as scrape_cord


bot = commands.Bot()


@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} is ready!")


@bot.slash_command(name="print-output")
async def print_output(ctx: discord.ApplicationContext, limit: int = 10, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    await ctx.respond(f"Printing last {limit} messages from {channel.mention}", ephemeral=True)

    data = await scrape_cord.scrap_channel(channel, limit)
    print(json.dumps(await data.export(), indent=4, sort_keys=True))


if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv("bot-token"))