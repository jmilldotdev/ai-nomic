import uuid
import aiohttp
import discord
from discord.ext import commands
from discord import Webhook

from ai_nomic import config
from ai_nomic.eden import act_as_agent, fetch_knowledge, interrogate_knowledge
from ai_nomic.models import AgenticPlayer


class AINomicCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.session_id = str(uuid.uuid4())
        self.agent_players = {}

    @commands.slash_command(
        name="rules",
        description="Display the full rules",
        guild_ids=config.ALLOWED_GUILDS,
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
        guild_ids=config.ALLOWED_GUILDS,
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
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def create_agent_player(
        self,
        ctx: commands.Context,
        name: discord.Option(str, description="The name of the agent player"),
        identity: discord.Option(str, description="The identity of the agent player"),
    ) -> None:
        agent = AgenticPlayer(name=name, identity=identity)
        self.agent_players[agent.name] = agent
        await ctx.respond(f"Created agent player {agent.name}")

    @commands.slash_command(
        name="remove_agent",
        description="Remove an agent player",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def remove_agent_player(
        self,
        ctx: commands.Context,
        name: discord.Option(str, description="The name of the agent player"),
    ) -> None:
        agent = self.agent_players.get(name)
        if not agent:
            await ctx.send(f"Agent player {name} not found")
            return
        del self.agent_players[agent.name]
        await ctx.respond(f"Removed agent player {agent.name}")

    @commands.slash_command(
        name="act_as_agent",
        description="Act as an agent player",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def act_as_agent_player(
        self,
        ctx: commands.Context,
        name: discord.Option(str, description="The name of the agent player"),
    ) -> None:
        await ctx.defer(ephemeral=True)
        try:
            agent = self.agent_players.get(name)
            if not agent:
                await ctx.send(f"Agent player {name} not found")
                return
            message = act_as_agent(agent.name, agent.identity)
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(config.DISCORD_WEBHOOK_URL, session=session)
                await webhook.send(message, username=agent.name)
            await ctx.respond(f"acted as agent player {name}")
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AINomicCog(bot))
