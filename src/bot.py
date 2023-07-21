import discord


async def run_command(message: discord.Message, command: str, *args: str):
    arg_refs = []
    for i, arg in enumerate(args):
        if arg.isnumeric():
            arg_refs.append(int(arg))
        elif arg.startswith("<@") and arg.endswith(">") and arg[2:-1].isnumeric():
            member = message.guild.get_member(int(arg[2:-1]))
            if not member:
                await message.reply(embed=discord.Embed(
                    title="ERROR",
                    description=f"Argument at position {i}: \"{arg}\" is invalid. No such member!",
                ))
                return
            arg_refs.append(member)
        elif arg.startswith("<#") and arg.endswith(">") and arg[2:-1].isnumeric():
            channel = message.guild.get_channel(int(arg[2:-1]))
            if not channel:
                await message.reply(embed=discord.Embed(
                    title="ERROR",
                    description=f"Argument at position {i}: \"{arg}\" is invalid. No such channel!",
                ))
                return
            arg_refs.append(channel)
        else:
            arg_refs.append(arg)
    return [command, arg_refs]


class Bot(discord.Bot):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)


BOT = Bot(intents=discord.Intents.all())
