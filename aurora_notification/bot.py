"""The implementation of the Discord bot that reports when the aurora is
likely to happen.
"""

import os
import sys
from typing import Optional

import discord  # type: ignore
import discord.ext.tasks  # type: ignore

from . import space_weather

intents = discord.Intents.default()

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# @tree.command(guild=client.guilds[0])
# async def slash(interaction: discord.Interaction, number: int, string: str):
#     await interaction.response.send_message(
#         f"{number=} {string=}", ephemeral=True
#     )


@discord.ext.tasks.loop(minutes=5)
async def check_for_weather_update(channel: discord.TextChannel):
    """Checks every few minutes for an update to the space weather."""
    aurora_activity = space_weather.aurora_activity_right_now()
    if aurora_activity is None:
        return
    await channel.send(
        f"{aurora_activity} with the aurora right now <@196169621525626880>!"
    )


@client.event
async def on_ready():
    """foo"""
    print(f"Client is logged in as {client.user}")
    output_channel: int = next(
        filter(
            lambda channel: channel.name == "testing",
            client.guilds[0].channels,
        ),
        None,
    )
    check_for_weather_update.start(output_channel)


async def main() -> None:
    """Main."""
    # with open(os.path.expanduser("~/.discord-bot"), "r") as discord_bot_file:
    #     bot_token = discord_bot_file.read()
    bot_token: Optional[str] = os.environ.get("DISCORD_BOT_TOKEN")
    if bot_token is None:
        print("DISCORD_BOT_TOKEN must be defined", file=sys.stderr)
        sys.exit(1)

    async with client:
        await client.start(bot_token)
