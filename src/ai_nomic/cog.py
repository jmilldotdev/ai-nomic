import random
import uuid
import aiohttp
import discord
from discord.ext import commands
from discord import Webhook

from ai_nomic import config
from ai_nomic.eden import (
    act_as_agent,
    interrogate_knowledge,
    vote_as_agent,
)
from ai_nomic.hedgedoc import get_doc_contents, new_hedgedoc
from ai_nomic.models import Player


class AINomicCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.session_id = str(uuid.uuid4())
        self.players = {}

    @commands.slash_command(
        name="initialize",
        description="Start a new game",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def initialize(self, ctx: commands.Context) -> None:
        try:
            self.players = {}
            if not self.bot.hedgedoc_url:
                self.bot.hedgedoc_url = new_hedgedoc()
            await ctx.respond(f"Initialized a new game. Rules can be found at {self.bot.hedgedoc_url}")
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")

    @commands.slash_command(
        name="add_player",
        description="Create a new player",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def add_player(
        self,
        ctx: commands.Context,
    ):
        try:
            name = str(ctx.author)
            player = Player(name=name)
            self.players[player.name] = player
            await ctx.respond(f"Created player {player.name}")
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")

    @commands.slash_command(
        name="remove_player",
        description="Remove a player",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def remove_player(
        self,
        ctx: commands.Context,
        name: discord.Option(str, description="The name of the player"),
    ) -> None:
        player = self.players.get(name)
        if not player:
            await ctx.send(f"Player {name} not found")
            return
        del self.players[player.name]
        await ctx.respond(f"Removed player {player.name}")

    @commands.slash_command(
        name="score",
        description="Display the score of all players",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def score(self, ctx: commands.Context) -> None:
        try:
            if len(self.players) == 0:
                await ctx.respond("No players registered yet")
                return
            score = "\n".join(
                [f"{player.name}: {player.score}" for player in self.players.values()]
            )
            await ctx.respond(score)
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")

    @commands.slash_command(
        name="rules",
        description="Display the full rules",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def rules(self, ctx: commands.Context) -> None:
        try:
            if not self.bot.hedgedoc_url:
                await ctx.respond("No game initialized yet")
                return
            await ctx.respond(f"Rules can be found at {self.bot.hedgedoc_url}")
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
            knowledge = get_doc_contents(self.bot.hedgedoc_url)
            answer = interrogate_knowledge(knowledge, question)
            await ctx.send(f"Inquiry: {question}\n\n{answer}")
            await ctx.respond("Done!")
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")

    @commands.slash_command(
        name="add_agent_player",
        description="Create a new agent player",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def add_agent_player(
        self,
        ctx: commands.Context,
        name: discord.Option(str, description="The name of the agent player"),
        identity: discord.Option(str, description="The identity of the agent player"),
    ) -> None:
        agent = Player(name=name, identity=identity, agent=True)
        self.players[agent.name] = agent
        await ctx.respond(f"Created agent player {agent.name}\n\n'{agent.identity}'")

    @commands.slash_command(
        name="agent_propose",
        description="Act as an agent player",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def agent_propose(
        self,
        ctx: commands.Context,
        name: discord.Option(str, description="The name of the agent player"),
    ) -> None:
        await ctx.defer(ephemeral=True)
        try:
            agent = self.players.get(name)
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

    @commands.slash_command(
        name="agent_vote",
        description="Vote as an agent player",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def agent_vote(
        self,
        ctx: commands.Context,
        name: discord.Option(str, description="The name of the agent player"),
        proposal: discord.Option(str, description="The proposal to vote on"),
    ) -> None:
        await ctx.defer(ephemeral=True)
        try:
            agent = self.players.get(name)
            if not agent:
                await ctx.send(f"Agent player {name} not found")
                return
            message = vote_as_agent(agent.name, agent.identity, proposal)
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(config.DISCORD_WEBHOOK_URL, session=session)
                await webhook.send(message, username=agent.name)
            await ctx.respond(f"voted as agent player {name}")
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")

    @commands.slash_command(
        name="roll_dice",
        description="Roll dice. Optionally specify the number of dice and the number of sides",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def roll_dice(
        self,
        ctx: commands.Context,
        num_dice: discord.Option(
            int, description="The number of dice to roll", default=1
        ),
        num_sides: discord.Option(
            int, description="The number of sides on each die", default=6
        ),
    ) -> None:
        try:
            dice = [random.randint(1, num_sides) for _ in range(num_dice)]
            await ctx.respond(f"Rolled {num_dice}d{num_sides}: {dice}")
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")

    @commands.slash_command(
        name="update_score",
        description="Update the score of a player",
        guild_ids=config.ALLOWED_GUILDS,
    )
    async def update_score(
        self,
        ctx: commands.Context,
        name: discord.Option(str, description="The name of the player"),
        change: discord.Option(int, description="The the amount to change the score"),
    ) -> None:
        try:
            player = self.players.get(name)
            if not player:
                await ctx.send(f"Player {name} not found")
                return
            player.score += change
            await ctx.respond(
                f"Updated score of player {player.name} to {player.score}"
            )
        except Exception as e:
            await ctx.respond(f"Oh no! Something went wrong: {e}")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AINomicCog(bot))
