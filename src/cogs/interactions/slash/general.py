import os
import discord
from discord import app_commands
from discord.ext import commands


class SlashGeneral(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.slash_cmds = []

    async def get_all_app_commands(self):
        app_cmds = []
        cmds = await self.client.tree.fetch_commands(guild=discord.Object(id=self.client.config['guild_id']))
        for cmd in cmds:
            if any(isinstance(opt, app_commands.AppCommandGroup) for opt in cmd.options):
                app_cmds.extend(cmd.options)
            else:
                app_cmds.append(cmd)
        return app_cmds

    def help_embed_gen(self, page):
        embed = discord.Embed(title='Help' , color=0xbd2b1c)
        if self.client.user.avatar:
            embed.set_thumbnail(url=self.client.user.avatar.url)
        for cmd in self.slash_cmds[page * 5 - 5:page * 5]:
            embed.add_field(name=cmd.mention, value=cmd.description, inline=False)
        pages = len(self.slash_cmds) // 5 + 1
        if len(self.slash_cmds) % 5 == 0:
            pages -= 1
        embed.set_footer(text=f'Page {page} of {pages}')
        return embed

    @app_commands.command(name="ping", description="Get the bot's latency")
    async def ping_slash(self, ctx: discord.Interaction):
        await ctx.response.defer()
        await ctx.followup.send(
            content=f"Pong!!!\nPing = `{round(self.client.latency * 1000)}ms`"
        )

    @app_commands.command(name="help", description="To get help on how to use the bot.")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.slash_cmds = await self.get_all_app_commands()
        embed = self.help_embed_gen(1)
        if self.client.user.avatar:
            embed.set_thumbnail(url=self.client.user.avatar.url)
        pages = len(self.slash_cmds) // 5 + 1
        if len(self.slash_cmds) % 5 == 0:
            pages -= 1
        view = Pagination(pages, self.help_embed_gen, interaction)
        await interaction.followup.send(embed=embed, view=view)


async def setup(client: commands.Bot):
    await client.add_cog(SlashGeneral(client), guild=discord.Object(id=client.config['guild_id']))


class Pagination(discord.ui.View):
    def __init__(self, pages, em_gen_fn, interaction: discord.Interaction):
        super().__init__(timeout=120)
        self.cur_page = 1
        self.pages = pages
        self.org_interaction = interaction
        self.embedgen = em_gen_fn

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.org_interaction.edit_original_response(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == self.org_interaction.user.id:
            return True
        else:
            await interaction.response.send_message('You can\'t use this button.', ephemeral=True)
            return False

    @discord.ui.button(label='First', style=discord.ButtonStyle.grey, emoji="⏪", disabled=True, custom_id='first')
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.cur_page == 1:
            await interaction.response.send_message('You are already on the first page.', ephemeral=True)
        else:
            self.cur_page = 1
            button.disabled = True
            self.children[1].disabled = True
            self.children[2].disabled = False
            self.children[3].disabled = False
            await interaction.response.edit_message(embed=self.embedgen(self.cur_page), view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.grey, emoji="◀️", disabled=True)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.cur_page == 1:
            await interaction.response.send_message('You are already on the first page.', ephemeral=True)
        else:
            self.cur_page -= 1
            if self.cur_page == 1:
                button.disabled = True
                self.children[0].disabled = True
            self.children[2].disabled = False
            self.children[3].disabled = False
            await interaction.response.edit_message(embed=self.embedgen(self.cur_page), view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.grey, emoji="▶️", custom_id='next')
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.cur_page == self.pages:
            await interaction.response.send_message('You are already on the last page.', ephemeral=True)
        else:
            self.cur_page += 1
            if self.cur_page == self.pages:
                button.disabled = True
                self.children[3].disabled = True
            if self.cur_page > 1:
                self.children[0].disabled = False
                self.children[1].disabled = False
            await interaction.response.edit_message(embed=self.embedgen(self.cur_page), view=self)

    @discord.ui.button(label='Last', style=discord.ButtonStyle.grey, emoji="⏩")
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.cur_page == self.pages:
            await interaction.response.send_message('You are already on the last page.', ephemeral=True)
        else:
            self.cur_page = self.pages
            button.disabled = True
            self.children[2].disabled = True
            self.children[0].disabled = False
            self.children[1].disabled = False
            await interaction.response.edit_message(embed=self.embedgen(self.cur_page), view=self)

    @discord.ui.button(label='Close', style=discord.ButtonStyle.grey, emoji="❌")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        for i in self.children:
            i.disabled = True
        self.stop()
        await interaction.response.edit_message(view=self)
