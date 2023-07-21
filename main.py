import os
import re
from pathlib import Path

import discord

from src.bot import BOT, run_command
from src.commands import Command


with open(os.path.join(Path(__file__).resolve().parent, "token.txt"), "r") as fp:
    TOKEN = fp.readlines()[0]


@BOT.event
async def on_connect():
    print(f"--> The bot logged in as {BOT.user}.")


@BOT.event
async def on_ready():
    print("--> The bot is ready.")


@BOT.event
async def on_message(message: discord.Message):
    if not message.content.startswith("gdi:"):
        return
    await Command(
        message,
        *await run_command(
            message, *re.sub(r"\s+", " ", message.content[4:]).split(" ")
        ),
    ).run()


if __name__ == "__main__":
    BOT.run(TOKEN)
