import discord
from discord.ext import commands
from html2image import Html2Image
import asyncio
import json
import util
import random
import math

config = util.Config()

class Bingo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.field_path = config.asset_path / 'bingo_fields.json'
        self.raw_board = []
        self.hti = Html2Image()
        self.card_path = None
        self.html = """
        <!DOCTYPE HTML>
        <html>
            <head>
                <link rel='stylesheet' href={css}>
            <body>
                <table id='bingo-card'><tbody>{}</tbody></table>
            </body>
        </html>
        """
        with open(self.field_path, 'rt') as raw:
            self.fields = json.loads(raw.read())

    def _get_field_options(self) -> list:
        with open(self.field_path, 'rt') as raw:
            data = json.loads(raw.read())
        return data['options']

    def _update_field_options(self, options: list):
        with open(self.field_path, 'rt') as raw:
            data = json.loads(raw.read())
        with open(self.field_path, 'wt') as output:
            data['options'] = options
            output.write(json.dumps(data, indent=2))
        return

    def _gen_board(self):
        options = self._get_field_options()
        flattened_board = []
        board_html = []
        i = 0
        board_square = math.sqrt(self.fields['board_size'])
        self.hti.size = (int(board_square * 200), int(board_square * 200))
        while i < self.fields['board_size']:
            j = 0
            row = []
            while j < board_square:
                option = random.choice(options)
                flattened_board.append(option)
                row.append(option)
                options.remove(option)
                j += 1
                i += 1
            self.raw_board.append(row)
        return

    def _gen_html(self):
        row_html = "<tr class='row'>{}</tr>"
        cell_html = "<td class='cell'>{}</td>"
        rows = []
        for row in self.raw_board:
            columns = []
            for column in row:
                columns.append(cell_html.format(column))
            rows.append(row_html.format(''.join(columns)))
        with open(str((config.asset_path / 'bingo_card.css').absolute()), 'rt') as raw_css:
            return self.html.format(''.join(rows), css=str((config.asset_path / 'bingo_card.css').absolute()))

    def _render_card(self, html):
        name = 'bingo_card.png'
        self.hti.output_path = str(config.asset_path.absolute())
        image_path = config.asset_path / name
        self.hti.screenshot(html_str=html, css_file=str((config.asset_path / 'bingo_card.css').absolute()), save_as=name)
        return image_path

    @discord.slash_command(name='board', guild_ids=config.data['guilds'])
    async def board(self, ctx):
        if len(self.raw_board) <= 0:
            self._gen_board()
        if self.card_path == None:
            html = self._gen_html()
            self.card_path = self._render_card(html)
        file = discord.File(str(self.card_path.absolute()))
        return await ctx.respond(file=file)

    @discord.slash_command(name='addbingofield', guild_ids=config.data['guilds'])
    async def add_bingo_field(self, ctx, field):
        options = self._get_field_options()
        if field in options:
            await ctx.respond(f'The field "{field}" already exists')
            return
        options.append(field)
        self._update_field_options(options)
        await ctx.respond(f'The field "{field}" was successfully added.')
        return

    @discord.slash_command(name='removebingofield', guild_ids=config.data['guilds'])
    async def add_bingo_field(self, ctx, field):
        options = self._get_field_options()
        if field not in options:
            await ctx.respond(f'The field "{field}" does not exist')
            return
        options.remove(field)
        self._update_field_options(options)
        await ctx.respond(f'The field "{field}" was successfully removed.')
        return

    @discord.slash_command(name='newboard', guild_ids=config.data['guilds'])
    async def new_board(self, ctx):
        self.raw_board = []
        self.card_path = None
        return await self.board(ctx)
