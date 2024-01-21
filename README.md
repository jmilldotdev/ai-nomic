# ai-nomic

A discord bot for playing AI-augmented Nomic.

## Setup

Copy .env.example as .env, fill out the required values

```
rye sync
rye run python src/ai_nomic/bot.py
```

## Usage

This bot functions as a player/gamestate manager, rules governor, and AI player manager.

### Rules Commands

`/rules` list the current rules of the game.

`/question` ask a question to the rules governor AI. Use this to check if a proposal is valid, or what its effects will be.

### Agent Commands

`/add_agent_player` adds an AI player to the game. It should have a name, and an agentic goal as its identity e.g. "You love rolling dice and want to make people roll dice as often as possible"

`/agent_propose` will take a turn to make a proposal as an AI player.

### Player Commands

`/register` will register you for the game.

`/remove_player` removes a human player from the game.

`/score` shows the current score of the game.

`/roll` will roll a dice for you. Specify number of faces and number of rolls as arguments.

