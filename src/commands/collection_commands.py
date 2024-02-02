import random
from urllib import response
import lightbulb
import hikari
from lightbulb import commands
import redis
import dyce
from ..dice import DicePool, Dice
import uuid

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
    deck_exists_message = ''
    deck_map_key = f"decks:{guild_id}:{user_id}:deck_map"
    if r.hexists(deck_map_key, name):
        # get deck
        deck_exists_message = f"Deck {name} already exists. Overwriting deck.\n Previous deck: \n{r.hget(deck_map_key, name)}"

    # create deck
    r.hset(deck_map_key, name, card_list)

    # respond
    await ctx.respond(f"Deck {name} created.\n{deck_exists_message}")

@lightbulb.option("name", "The name of the deck.", required=True)
@lightbulb.option("card_list", "The list of cards to create a deck from. Seperated by a comma (,)", required=True)
@lightbulb.command("create_guild_deck", "Creates a deck of cards with the given list for the whole guild.", ephemeral=True)
@lightbulb.implements(commands.SlashCommand)
async def create_guild_deck(ctx: lightbulb.context.Context):
    card_list = ctx.options.card_list
    name = ctx.options.name

    # get redis
    rpool = ctx.bot.redis_pool
    r = redis.Redis(connection_pool=rpool)

    # get guild id
    guild_id = ctx.guild_id

    # check if deck exists
    deck_exists_message = ''
    deck_map_key = f"decks:{guild_id}:deck_map"
    if r.hexists(deck_map_key, name):
        # get deck
        deck_exists_message = f"Deck {name} already exists. Overwriting deck.\n Previous deck: \n{r.hget(deck_map_key, name)}"

    # create deck
    r.hset(deck_map_key, name, card_list)

    # respond
    await ctx.respond(f"Deck {name} created for the whole guild.\n{deck_exists_message}")

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

        # check if guild deck exists
        guild_deck_map_key = f"decks:{guild_id}:deck_map"
        if r.hexists(guild_deck_map_key, name):
            card_string = r.hget(guild_deck_map_key, name)
        else:
            # check if user deck exists
            user_deck_map_key = f"decks:{guild_id}:{user_id}:deck_map"
            if not r.hexists(user_deck_map_key, name):
                await ctx.respond(f"Deck {name} does not exist.", flags=hikari.MessageFlag.EPHEMERAL)
                return
            # get deck
            card_string = r.hget(user_deck_map_key, name)

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
@lightbulb.option("include_cards", "Whether to include the associated list of cards.", bool, default=False)
@lightbulb.command("list_decks", "Lists the names of each deck.", ephemeral=True)
@lightbulb.implements(commands.SlashCommand)
async def list_decks(ctx: lightbulb.context.Context):
    include_cards = ctx.options.include_cards

    # get redis
    rpool = ctx.bot.redis_pool
    r = redis.Redis(connection_pool=rpool)

    # get guild id
    guild_id = ctx.guild_id
    # get user id
    user_id = ctx.author.id

    # get deck map key
    deck_map_key = f"decks:{guild_id}:{user_id}:deck_map"

    # get deck names
    deck_names = r.hkeys(deck_map_key)

    response = "Decks:\n"
    for deck_name in deck_names:
        deck_name = deck_name
        response += deck_name
        if include_cards:
            card_list = r.hget(deck_map_key, deck_name)
            response += f" ({card_list})"
        response += "\n"
    
    # check response lenth, if over 2000 characters, make into a text file
    if len(response) > 2000:
        # create txt file and put response in it
        filename = f"{uuid.uuid4()}_decks.txt"
        with open(filename, 'w') as wf:
            wf.write(response)
        
        # create new response, attach file to it, and send
        response = "Deck list too long. See text file for full list."
        file = hikari.File(filename)
        await ctx.respond(response, attachment=file)
        os.remove(filename)
        return

    await ctx.respond(response)

# list guild decks
@lightbulb.option("include_cards", "Whether to include the associated list of cards.", bool, default=False)
@lightbulb.option("ephemeral", "Whether the response should be ephemeral.", bool, default=True)
@lightbulb.command("list_guild_decks", "Lists the names of each deck for the whole guild.")
@lightbulb.implements(commands.SlashCommand)
async def list_guild_decks(ctx: lightbulb.context.Context):
    include_cards = ctx.options.include_cards
    ephemeral = ctx.options.ephemeral

    # get redis
    rpool = ctx.bot.redis_pool
    r = redis.Redis(connection_pool=rpool)

    # get guild id
    guild_id = ctx.guild_id

    # get deck map key
    deck_map_key = f"decks:{guild_id}:deck_map"

    # get deck names
    deck_names = r.hkeys(deck_map_key)

    response = "Decks:\n"
    for deck_name in deck_names:
        deck_name = deck_name
        response += deck_name
        if include_cards:
            card_list = r.hget(deck_map_key, deck_name)
            response += f" ({card_list})"
        response += "\n"
    
    # check response length, if over 2000 characters, make into a text file
    if len(response) > 2000:
        # create txt file and put response in it
        filename = f"{uuid.uuid4()}_decks.txt"
        with open(filename, 'w') as wf:
            wf.write(response)
        
        # create new response, attach file to it, and send
        response = "Deck list too long. See text file for full list."
        file = hikari.File(filename)
        await ctx.respond(response, attachment=file, flags=hikari.MessageFlag.EPHEMERAL if ephemeral else None)
        os.remove(filename)
        return

    await ctx.respond(response, flags=hikari.MessageFlag.EPHEMERAL if ephemeral else None)

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
    bot.command(list_decks)
    bot.command(create_guild_deck)
    bot.command(list_guild_decks)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("deckofmany"))
    bot.remove_command(bot.get_slash_command("domtex"))
    bot.remove_command(bot.get_slash_command("tarot"))
    bot.remove_command(bot.get_slash_command("create_deck"))
    bot.remove_command(bot.get_slash_command("draw_cards"))
    bot.remove_command(bot.get_slash_command("list_decks"))
    bot.remove_command(bot.get_slash_command("create_guild_deck"))
    bot.remove_command(bot.get_slash_command("list_guild_decks"))