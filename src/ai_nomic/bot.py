import argparse
import discord
from discord.ext import commands
from ai_nomic.config import DISCORD_TOKEN


class AINomicClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")


class AINomicBot(commands.Bot):
    def __init__(self, hedgedoc_url=None) -> None:
        intents = discord.Intents.default()
        self.set_intents(intents)
        self.hedgedoc_url = hedgedoc_url
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
        if self.hedgedoc_url:
            print("Using existing hedgedoc: ", self.hedgedoc_url)
        print("Running bot...")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        await self.process_commands(message)


def start(hedgedoc_url: str = None) -> None:
    print("Launching bot...")
    bot = AINomicBot(hedgedoc_url)
    bot.load_extension("ai_nomic.cog")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the bot")
    parser.add_argument("--hedgedoc-url", type=str, help="The URL of the hedgedoc to use")
    args = parser.parse_args()
    start(args.hedgedoc_url)
