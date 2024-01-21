import discord
from discord.ext import commands
from ai_nomic.config import DISCORD_TOKEN


class AINomicClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")


class AINomicBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        self.set_intents(intents)
        commands.Bot.__init__(
            self,
            command_prefix="!",
            intents=intents,
        )

    def set_intents(self, intents: discord.Intents) -> None:
        intents.message_content = True
        intents.messages = True
        intents.presences = True
        intents.members = True

    async def on_ready(self) -> None:
        print("Running bot...")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        await self.process_commands(message)


def start() -> None:
    print("Launching bot...")
    bot = AINomicBot()
    bot.load_extension("ai_nomic.cog")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    start()
