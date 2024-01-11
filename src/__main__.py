import video
import discord
import os
import json
import threading
import queue
import pathlib
#import discord_events
import asyncio
import util
from discord.ext import commands
import cogs
#bot permissions integer: 274878016512
#bot invite link is: https://discord.com/api/oauth2/authorize?client_id=1151607164817915965&permissions=274878016512&scope=bot%20applications.commands

render_queue = queue.Queue()

config = util.Config()

intents = discord.Intents(messages=True, guilds=True, typing=True, message_content=True)
client = commands.Bot(intents=intents, command_prefix='/')

def render(clip: video.TurnClip):
    success, value = clip.composite()
    render_queue.put((success, value))
    return

@client.command(name="turn", guild_ids=config.data['guilds'])
async def turn(ctx: commands.Context):
    name = ctx.message.content.replace('/turn ', '', 1)
    clip = video.TurnClip(name)
    render_thread = threading.Thread(target=render, args=[clip])
    render_thread.start()
    while True:
        try:
            data = render_queue.get(block=False)
        except queue.Empty:
            asyncio.sleep(1)
            continue
        if data[0] == True:
            video_file = discord.File(str(data[1]))
            await ctx.channel.send(file=video_file)
            await ctx.message.delete()
        else:
            await ctx.respond(f'An error occurred while trying to create the clip:\n```{data[1]}```')
        break
    render_thread.join()
    #await ctx.respond(file=video_file)
    return

@client.event
async def on_ready():
    #await client.add_cog(discord_events.ScheduledEvents(client, config['guildId']))
    print(f'Successfully connected to discord as {client.user}')

def main():
    client.add_cog(cogs.Bingo(client))
    client.add_cog(cogs.Map(client))
    client.run(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    main()