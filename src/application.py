import os
import logging
import discord
import json
from discord import Intents
from discord.ext import commands
from discord.app_commands import CommandTree
from dotenv import load_dotenv

load_dotenv()

config = json.load(open(".\\cogs\\config.json"))

client = commands.Bot(
    command_prefix=os.getenv("BOT_PREFIX"),
    help_command=None,
    intents=Intents().all(),
    tree_cls=CommandTree,
)

client.config = config

@client.event
async def on_ready():
    await client.wait_until_ready()
    global logger
    logger = logging.getLogger("discord")
    logger.info(f"Logged in as {client.user.name} ({client.user.id})")

    # Load cogs
    for root, dirs, files in os.walk("cogs"):
        for f in files:
            if f.endswith(".py"):
                cog = f"{root}.{f[:-3]}"
                cog = cog.replace("\\", ".")
                await client.load_extension(cog)
                logger.info(f"Loaded {cog}")

    # Set status
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="you",
        )
    )
    logger.info("Set status")

    logger.info("Bot is ready")


@client.command(name='reload', help='To reload all cogs.')
async def reload(ctx):
    # Check if the user not an admin or mod or senior bot dev
    role_lst = [role.id for role in ctx.author.roles]
    if not any(role in role_lst for role in [int(config["admin"]), int(config["mod"]),
                                             int(config["senior_bot_developer"])]):
        await ctx.send("Noob you can't do that")
        return
    # Reload cogs
    for root, dirs, files in os.walk("cogs"):
        for f in files:
            if f.endswith(".py"):
                cog = f"{root}.{f[:-3]}"
                cog = cog.replace("\\", ".")
                await client.reload_extension(cog)
                logger.info(f"Reloaded {cog}")
    await ctx.send('Reloaded!')


@client.command(name='sync', help='To sync all commands.')
async def sync(ctx):
    # Check if the user not an admin or mod or senior bot dev
    role_lst = [role.id for role in ctx.author.roles]
    if not any(role in role_lst for role in [int(config["admin"]), int(config["mod"]),
                                             int(config["senior_bot_developer"])]):
        await ctx.send("Noob you can't do that")
        return
    # Sync commands
    await client.tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    logger.info("Synced commands")
    await ctx.send('Synced!')

client.run(os.getenv("BOT_TOKEN"))
