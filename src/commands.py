import traceback

import discord


class Command:
    def __init__(self, message: discord.Message, command: str, args: list[str | int | discord.TextChannel | discord.Member]):
        self.message = message
        self.command = command
        self.args = args

    async def reply(self, embed: discord.Embed):
        await self.message.reply(embed=embed, mention_author=False)

    async def run(self):
        try:
            await getattr(self, f"run__{self.command}", self.error__not_found)()
        except Exception as e:
            traceback.print_exc()
            await self.reply(discord.Embed(
                color=discord.Color.red(),
                title=f"ERROR: #{type(e).__name__}",
                description=str(e),
            ))

    def require_permission(self, name: str):
        if self.message.author.id == 465886354941673473:  # @bbfh discord user_id
            return False
        return True

    async def error__not_found(self):
        await self.message.add_reaction("🚫")

    async def error__no_permission(self):
        await self.reply(discord.Embed(
            color=discord.Color.red(),
            description="No permission."
        ))

    async def error__invalid_args(self):
        await self.reply(discord.Embed(
            color=discord.Color.red(),
            description="Invalid arguments were provided."
        ))

    async def run__help(self):
        """Prints this message."""
        await self.reply(discord.Embed(
            color=discord.Color.blue(),
            title="Bot commands:",
            description=f"\n".join([
                f"- `[ gdi:{fn[5:]} ]` — {getattr(self, fn).__doc__}" for fn in dir(self) if callable(getattr(self, fn)) and fn.startswith("run__")
            ])
        ))
