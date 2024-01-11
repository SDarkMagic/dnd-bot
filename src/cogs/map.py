import discord
from discord.ext import commands
import asyncio
import util
import pathlib

config = util.Config()

class MapCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        #self.guilds = guilds
        self.map_path = config.asset_path / 'tolg_map.png'
        self.bot = bot

    @discord.slash_command(name='map', guild_ids=config.data['guilds'])
    async def map(self, ctx: commands.Context):
        path = self.map_path
        file = discord.File(str(path.absolute()))
        await ctx.respond(file=file)
        return

    @discord.slash_command(name='uploadmap', guild_ids=config.data['guilds'])
    async def upload_map(self, ctx: commands.Context, file: discord.Attachment):
        path = self.map_path
        if (file.content_type != 'image/png'):
            await ctx.respond('Please provide a valid file...')
            return
        await file.save(path)
        await ctx.respond('Succesfully updated the map!')
        return