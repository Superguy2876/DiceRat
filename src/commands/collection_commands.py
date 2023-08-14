import random
from urllib import response
import lightbulb
import hikari
from lightbulb import commands
import redis
import dyce
from ..dice import DicePool, Dice

# deck of many things bot function
@lightbulb.option("number", "The number of cards to pull.", int, default=1)
@lightbulb.command("deckofmany", "Pull a card from the deck of many things.")
@lightbulb.implements(commands.SlashCommand)
async def deckofmany(ctx: lightbulb.context.Context) -> None:
    number = ctx.options.number

    deck = [
        "Vizier",
        "Sun",
        "Moon",
        "Star",
        "Comet",
        "The Fates",
        "Throne",
        "Key",
        "Knight",
        "Gem",
        "Talons",
        "The Void",
        "Flames",
        "Skull",
        "Idiot",
        "Donjon",
        "Ruin",
        "Euryale",
        "Rogue",
        "Balance",
        "Fool",
        "Jester"
    ]

    cards = []

    try:
        cards = random.sample(deck, k=number)
    except ValueError:
        await ctx.respond("Invalid number of cards.", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    new_line = "\n"
    response = f"Pulling {number} cards.\n"
    response += f"{new_line.join(cards)}"

    await ctx.respond(response)


# deck of many things bot function
@lightbulb.option("number", "The number of cards to pull.", int, default=1)
@lightbulb.command("domtex", "Pull a card from an expanded deck of many things.")
@lightbulb.implements(commands.SlashCommand)
async def domtex(ctx: lightbulb.context.Context) -> None:
    number = ctx.options.number

    deck = [
            "The Donjon",
            "Ruin",
            "The Euryale",
            "The Rouge",
            "The Magician",
            "The Chariot",
            "Justice",
            "Temperance",
            "Judgment",
            "The World",
            "Woe",
            "The Wings",
            "Balance",
            "The Fates",
            "The Throne",
            "The Key",
            "The Knight",
            "The High Priestess",
            "The Lovers",
            "Wheel of Fortune",
            "Death",
            "Metamorphosis",
            "The Recluse",
            "Fashionable",
            "The Hermaphrodite",
            "The Gem",
            "The Talons",
            "The Void",
            "The Flames",
            "The Skull",
            "The Hierophant",
            "The Hermit",
            "The Hanged Man",
            "The Tired",
            "The Enamoured",
            "The Clumsy",
            "The Weak",
            "The Dull",
            "The Idiot",
            "The Vizier",
            "The Sun",
            "The Moon",
            "The Star",
            "The Empress",
            "The Emperor",
            "The Strong",
            "The Resilient",
            "The Livly",
            "The Trusted",
            "The All Seeing",
            "The Courier",
            "The Comet",
            "The Fool",
            "The Jester"
            ]

    cards = []

    try:
        cards = random.sample(deck, k=number)
    except ValueError:
        await ctx.respond("Invalid number of cards.", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    new_line = "\n"
    response = f"Pulling {number} cards.\n"
    response += f"{new_line.join(cards)}"

    await ctx.respond(response)

# tarot card bot function
@lightbulb.option("number", "The number of cards to pull.", int, default=1)
@lightbulb.command("tarot", "Pull a tarot card.")
@lightbulb.implements(commands.SlashCommand)
async def tarot(ctx: lightbulb.context.Context) -> None:
    number = ctx.options.number
    if number <= 0:
        await ctx.respond("Invalid number of cards.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    deck = [
        "The Fool",
        "The Magician",
        "The High Priestess",
        "The Empress",
        "The Emperor",
        "The Hierophant",
        "The Lovers",
        "The Chariot",
        "Strength",
        "The Hermit",
        "Wheel of Fortune",
        "Justice",
        "The Hanged Man",
        "Death",
        "Temperance",
        "The Devil",
        "The Tower",
        "The Star",
        "The Moon",
        "The Sun",
        "Judgement",
        "The World"
    ]

    cards = []

    try:
        cards = random.sample(deck, k=number)
    except ValueError:
        await ctx.respond("Invalid number of cards.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    new_line = "\n"
    response = f"Pulling {number} cards.\n"
    response += f"{new_line.join(cards)}"

    await ctx.respond(response)

# Creates a deck of cards from a list of cards
# Stores the deck in a redis cache
@lightbulb.option("name", "The name of the deck.", required=True)
@lightbulb.option("card_list", "The list of cards to create a deck from. Seperated by a comma (,)", required=True)
@lightbulb.command("create_deck", "Creates a deck of cards with the given list.", ephemeral=True)
@lightbulb.implements(commands.SlashCommand)
async def create_deck(ctx: lightbulb.context.Context):
    card_list = ctx.options.card_list
    name = ctx.options.name

    # get redis
    rpool = ctx.bot.redis_pool
    r = redis.Redis(connection_pool=rpool)

    # get guild id
    guild_id = ctx.guild_id
    # get user id
    user_id = ctx.author.id
    # check if deck exists
    desk_exists_message = ''
    if r.exists(f"deck:{guild_id}:{user_id}:{name}"):
        # get deck
        desk_exists_message = f"Deck {name} already exists. Overwriting deck.\n Previous deck: \n{r.get(f'deck:{guild_id}:{user_id}:{name}')}"

    # create deck
    r.set(f"deck:{guild_id}:{user_id}:{name}", card_list)

    # respond
    await ctx.respond(f"Deck {name} created.\n{desk_exists_message}")

@lightbulb.option("name", "The name of the deck to draw from. Ignores card list if specified.", default=None)
@lightbulb.option("number", "The number of cards to draw.", int, default=1)
@lightbulb.option("card_list", "The list of cards to draw from. Seperated by a comma (,)", default=None)
@lightbulb.command("draw_cards", "Draws a number of cards from a deck.")
@lightbulb.implements(commands.SlashCommand)
async def draw_cards(ctx: lightbulb.context.Context):
    number = ctx.options.number
    card_string = ctx.options.card_list
    name = ctx.options.name

    # get redis if deck name is specified
    if name is not None:
        rpool = ctx.bot.redis_pool
        r = redis.Redis(connection_pool=rpool)
        # get guild id
        guild_id = ctx.guild_id
        # get user id
        user_id = ctx.author.id
        # check if deck exists
        if not r.exists(f"deck:{guild_id}:{user_id}:{name}"):
            await ctx.respond(f"Deck {name} does not exist.", flags=hikari.MessageFlag.EPHEMERAL)
            return
        # get deck
        card_string = r.get(f"deck:{guild_id}:{user_id}:{name}")
    
    card_list = card_string.split(",")
    # remove empty strings, and leading and trailing spaces
    card_list = [card.strip() for card in card_list if card.strip()]

    try:
        cards = random.sample(card_list, k=number)
    except ValueError:
        await ctx.respond("Invalid number of cards.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    new_line = "\n"
    response = f"Pulling {number} cards.\n"
    response += f"{new_line.join(cards)}"

    await ctx.respond(response)

# Pulls a number cards from a deck of cards
def pullCards(deck, number):
    cards = []
    if number > len(deck):
        raise ValueError("Not enough cards in deck.")
    for _ in range(number):
        cards.append(deck.pop())
    return cards


def load(bot: lightbulb.BotApp) -> None:
    bot.command(deckofmany)
    bot.command(domtex)
    bot.command(tarot)
    bot.command(create_deck)
    bot.command(draw_cards)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("deckofmany"))
    bot.remove_command(bot.get_slash_command("domtex"))
    bot.remove_command(bot.get_slash_command("tarot"))
    bot.remove_command(bot.get_slash_command("create_deck"))
    bot.remove_command(bot.get_slash_command("draw_cards"))