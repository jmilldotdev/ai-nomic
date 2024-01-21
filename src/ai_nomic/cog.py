import uuid
import discord
from discord.ext import commands

from ai_nomic.config import ALLOWED_GUILDS
from ai_nomic.eden import fetch_knowledge, interrogate_knowledge


class AINomicCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.session_id = str(uuid.uuid4())

    @commands.slash_command(
        name="rules",
        description="Display the full rules",
        guild_ids=ALLOWED_GUILDS,
    )
    async def rules(self, ctx: commands.Context) -> None:
        try:
            await ctx.defer(ephemeral=True)
            rules_chunks = fetch_knowledge()
            for chunk in rules_chunks:
                await ctx.send(chunk)
        except Exception as e:
            await ctx.send(f"Oh no! Something went wrong: {e}")

    @commands.slash_command(
        name="question",
        description="Ask a question regarding the rules, or about a proposal",
        guild_ids=ALLOWED_GUILDS,
    )
    async def rules_question(
        self,
        ctx: commands.Context,
        question: discord.Option(str, description="Your question"),
    ) -> None:
        try:
            await ctx.defer(ephemeral=True)
            answer = interrogate_knowledge(question, self.session_id)
            await ctx.send(f"Inquiry: {question}\n\n{answer}")
            await ctx.respond("Done!")
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")

    @commands.slash_command(
        name="create_agent",
        description="Create a new agent player",
        guild_ids=ALLOWED_GUILDS,
    )
    async def create_agent_player(self, ctx: commands.Context) -> None:
        await ctx.send("Hello, World!")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AINomicCog(bot))
