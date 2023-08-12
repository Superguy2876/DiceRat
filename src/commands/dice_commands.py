import random
from urllib import response
import lightbulb
from lightbulb import commands
import redis
import dyce
from ..dice import DicePool, Dice


# These two are the same type, but are optional. We can provide a
# default value simply by using the `default` kwarg.
@lightbulb.option("dice", "The dice to be rolled, will roll a single d20 if no value provided.", str, default='1d20')
@lightbulb.option("label", "The call the dice string saved to a label, dice field will be ignored.", str, default='')
@lightbulb.option("options", "The options to modify the type of dice roll.", str, default='')
@lightbulb.command("roll", "Roll one or more dice.")
# Define the types of command that this function will implement
@lightbulb.implements(commands.SlashCommand)
async def dice(ctx: lightbulb.context.Context) -> None:
    # Extract the options from the context
    dice = ctx.options.dice
    options = ctx.options.options
    label = ctx.options.label

    if label:
        # get dice string from redis
        r = redis.Redis(connection_pool=ctx.bot.redis_pool)
        # get user id
        user_id = str(ctx.author.id)
        # get guild id
        guild_id = str(ctx.guild_id)
        # create key
        key = f"{guild_id}:{user_id}:{label}"

        if not r.exists(key):
            ctx.command.default_ephemeral = True
            await ctx.respond(f"Error: No dice string saved to label {label}")
            return

        dice = r.get(key)
    dice_pool = DicePool(dice)

    try:
        dice_pool = DicePool(dice)
    except Exception as e:
        # send ephemeral error message
        ctx.command.default_ephemeral = True
        await ctx.respond(f"Error: {e}, Invalid Dice String")
        return
    dice_pool.roll()

    if ('a' in options) != ('d' in options):
        bonus_pool = DicePool(dice)
        bonus_pool.roll()
        if 'a' in options:
            if dice_pool.total < bonus_pool.total:
                dice_pool = bonus_pool
            else:
                dice_pool = dice_pool
        else:
            if dice_pool.total > bonus_pool.total:
                dice_pool = bonus_pool
            else:
                dice_pool = dice_pool
               
    
    # find maximum digit in options
    reroll_value = max((int(ch) for ch in options if ch.isdigit()), default=0)

    if reroll_value:
        dice_pool.reroll(lambda x: x <= reroll_value)

    options_string = ''
    if 'a' in options:
        options_string += 'Advantage, '
    if 'd' in options:
        options_string += 'Disadvantage, '
    if reroll_value:
        options_string += f'Rerolling {reroll_value} or lower'
    # Create a response string
    response = f"Rolling {dice}, {options_string}\n"

    for item in dice_pool.look():
        dice_str_list = []
        if isinstance(item, dict):
            dice_str_list.append(f"{item['quantity']}d{item['sides']}:({', '.join(str(x) for x in item['values'])} : {item['total']})")
        else:
            dice_str_list.append(str(item))
        response += f"{'+ '.join(dice_str_list)}"
    
    response += f" = {dice_pool.total}"

    if len(response) > 2000:
        response = f"Dice roll body too long.\nRolling {dice}, {options_string}\nTotal: {dice_pool.total}"


    await ctx.respond(response)

@lightbulb.option("label", "The label for the dice string.", str, required=True)
@lightbulb.option("dice", "The dice to be rolled, will roll a single d20 if no value provided.", str, required=True)
@lightbulb.command("create_label", "Create a label for dice string.", ephemeral=True)
@lightbulb.implements(commands.SlashCommand)
async def create_label(ctx: lightbulb.context.Context) -> None:
    try:
        dice_pool = DicePool(ctx.options.dice)
    except Exception as e:
        # send ephemeral error message
        ctx.command.default_ephemeral = True
        await ctx.respond(f"Error: {e}, Invalid Dice String")
        return

    label = ctx.options.label
    # get user id
    user_id = ctx.author.id
    # get guild id
    guild_id = ctx.guild_id
    # create redis connection
    r = redis.Redis(connection_pool=ctx.bot.redis_pool)
    # create key
    key = f"{guild_id}:{user_id}:{label}"
    # check if key exists
    existing_dice_string = ''
    if r.exists(key):
        existing_dice_string = f' overwriting existing dice string: {r.get(key)}'
        
    # set key
    r.set(key, ctx.options.dice)
    await ctx.respond(f"Label {label} created. {existing_dice_string}")


@lightbulb.option("coins", "The number of coins to flip.", int, default=1)
@lightbulb.command("flip", "Flip some coins.")
@lightbulb.implements(commands.SlashCommand)
async def flip(ctx: lightbulb.context.Context) -> None:
    coins = ctx.options.coins
    if coins <= 0:
        await ctx.respond("Invalid number of coins.")
        return
    
    flipList = []
    heads = 0
    tails = 0
    for _ in range(coins):
        flipList.append(random.choice(["Heads", "Tails"]))
        if flipList[-1] == "Heads":
            heads += 1
        else:    
            tails += 1
    
    response = f"Flipping {coins} coins.\n"
    response += f"Flipped {heads} heads and {tails} tails.\n"
    response += f"{', '.join(flipList)}"

    if len(response) > 2000:
        response = f"Coin flip body too long.\nFlipping {coins} coins.\n Total Heads: {heads}, Total Tails: {tails}."
    
    await ctx.respond(response)



@lightbulb.option("modifier", "The modifier to be added to the roll.", int, default=0)
@lightbulb.option("options", "The options to modify the type of dice roll.", str, default='')
@lightbulb.command("r20", "Roll a d20 with modifiers.")
@lightbulb.implements(commands.SlashCommand)
async def r20(ctx: lightbulb.context.Context) -> None:
    modifier = ctx.options.modifier
    options = ctx.options.options

    if 'a' in options and 'd' in options:
        options = ''

    
    rolls = [random.randint(1, 20), random.randint(1, 20)]
    
    if 'a' in options:
        roll = max(rolls)
        discardedRoll = min(rolls)
        optionsText = " with advantage"
        rollText = f"({roll}, ~~{discardedRoll}~~)"
    
    elif 'd' in options:
        roll = min(rolls)
        discardedRoll = max(rolls)
        optionsText = " with disadvantage"
        rollText = f"({roll}, ~~{discardedRoll}~~)"

    else:
        roll = rolls[0]
        discardedRoll = 0
        optionsText = ""
        rollText = f"({roll})"
    
    responseHead = f"Rolling a d20{optionsText} + {modifier}:\n"
    responseBody = f"{rollText} + {modifier} = {roll + modifier}"

    await ctx.respond(responseHead + responseBody)


# tarot card bot function
@lightbulb.option("number", "The number of cards to pull.", int, default=1)
@lightbulb.command("tarot", "Pull a tarot card.")
@lightbulb.implements(commands.SlashCommand)
async def tarot(ctx: lightbulb.context.Context) -> None:
    number = ctx.options.number
    if number <= 0:
        await ctx.respond("Invalid number of cards.")
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
        await ctx.respond("Invalid number of cards.")
        return

    new_line = "\n"
    response = f"Pulling {number} cards.\n"
    response += f"{new_line.join(cards)}"

    await ctx.respond(response)

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
        await ctx.respond("Invalid number of cards.")
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
        await ctx.respond("Invalid number of cards.")
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

@lightbulb.command("test", "test command")
@lightbulb.implements(commands.SlashCommand)
async def test(ctx: lightbulb.context.Context) -> None:
    
    rpool = ctx.bot.redis_pool
    r = redis.Redis(connection_pool=rpool)
    r.set("test", "test061")
    r_test = r.get("test")
    await ctx.respond(f'{r_test}')

def load(bot: lightbulb.BotApp) -> None:
    bot.command(dice)
    bot.command(r20)
    bot.command(flip)
    bot.command(tarot)
    bot.command(deckofmany)
    bot.command(domtex)
    bot.command(test)
    bot.command(create_label)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("dice"))
    bot.remove_command(bot.get_slash_command("r20"))
    bot.remove_command(bot.get_slash_command("flip"))
    bot.remove_command(bot.get_slash_command("tarot"))
    bot.remove_command(bot.get_slash_command("deckofmany"))
    bot.remove_command(bot.get_slash_command("domtex"))
    bot.remove_command(bot.get_slash_command("test"))
    bot.remove_command(bot.get_slash_command("create_label"))





