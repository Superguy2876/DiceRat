import random
from urllib import response
import lightbulb
import hikari
from lightbulb import commands
import redis
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


def send_and_receive(client, messages):
    return client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

@lightbulb.option("Choice", "Choose your object.", str, required=True)
@lightbulb.command("SPR", "Enter a Custom Scissors, Paper, Rock Game.")
@lightbulb.implements(commands.SlashCommand)
async def scissors_paper_rock(ctx: lightbulb.context.Context) -> None:
    user_choice = ctx.options.choice.lower()

    guild_id = ctx.get_guild().id
    key = f"{guild_id}:SPR"

    r = redis.Redis(connection_pool=ctx.bot.redis_pool)

    existing_challenge = r.get(key)

    if existing_challenge is None:
        r.set(key, user_choice)
        await ctx.respond("SPR challenge started! Waiting for another player.")
        return
    

    # If we're here, it means that there is an existing challenge.
    await ctx.respond("A challenge has begun. Please wait for the results.")
    players = [existing_challenge, user_choice]

    # We can use the OpenAI API to generate a response.
    # You can use the `send_and_receive` function above to do this.
    # Setup the system first.
    client = OpenAI()

    system_message = {'role':'system'}
    system_message['content'] = """You are a god of chaos. 
    You are Sarcastic, humorous, and a bit of a trickster. 
    You are called to adjudicate a game of Scissors, Paper, Rock between two players.
    The catch being that the players can choose ANYTHING as their object.
    Decide who wins the game. A describe why and how they won in a humours manner.
    Use the following format:
    Player 1: <object>
    Player 2: <object>
    Winner: <player>
    Reason: <reason>
    """
    user_message = {'role':'user'}

    user_message['content'] = f"player1: {players[0]}\nplayer2: {players[1]}"
    messages = [system_message, user_message] 
    completion = send_and_receive(client, messages)
    response = completion.choices[0].message.content

    # Edit the message with the response.
    await ctx.edit_last_response(response)
    
    # You may want to clear the key after the game is done.
    r.delete(key)

def load(bot: lightbulb.BotApp) -> None:
    bot.command(scissors_paper_rock)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("SPR"))