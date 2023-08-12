import os
import logging
import discord
from discord import Intents
from discord.ext import commands
from discord.app_commands import CommandTree
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(
    command_prefix=os.getenv("BOT_PREFIX"),
    help_command=None,
    intents=Intents().all(),
    tree_cls=CommandTree,
)


@client.event
async def on_ready():
    await client.wait_until_ready()
    logger = logging.getLogger("discord")
    logger.info(f"Logged in as {client.user.name} ({client.user.id})")

    # Load cogs
    for root, dirs, files in os.walk("cogs"):
        for f in files:
            if f.endswith(".py"):
                cog = f"{root.replace('/', '.')}.{f[:-3]}"
                await client.load_extension(cog)
                logger.info(f"Loaded {cog}")

    # Sync commands
    await client.tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    logger.info("Synced commands")

    # Set status
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="you",
        )
    )
    logger.info("Set status")

    logger.info("Bot is ready")


client.run(os.getenv("BOT_TOKEN"))
