# ScrapeCord

ScrapeCord is a python library for generating and rendering transcripts of discord channels from a py-cord discord bot.

ScrapeCord collects data from a discord channel and stores it in a [json-format](JSON-FORMAT.md). This [json-format](JSON-FORMAT.md) data then can be rendered to html.


## Scraping
```python
from ScrapeCord.scraper import Scraper

@bot.slash_command(name="example")
async def print_output(ctx: discord.ApplicationContext, limit: int = 10, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    await ctx.respond(f"Scaped {limit} messages from {channel.mention}", ephemeral=True)

    scraper = Scraper(channel, limit)
    data = await scraper.scrape_channel()
    json_string = json.dumps(data, indent=4, sort_keys=True)
    print(json_string)

    with open("example.json", "w", encoding="utf-8") as f:
        f.write(json_string)
```


## Rendering
```python
from ScrapeCord.renderer import render_to_html

with open("example.json", "r") as f:
    data = json.load(f)

html = render_to_html(data)

with open("example.html", "w", encoding="utf-8") as f:
    f.write(html)
```
