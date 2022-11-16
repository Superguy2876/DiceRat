import random
from urllib import response
import lightbulb
from lightbulb import commands


# These two are the same type, but are optional. We can provide a
# default value simply by using the `default` kwarg.
@lightbulb.option("dice", "The dice to be rolled, will roll a single d20 if no value provided.", str, default='1d20')
@lightbulb.option("options", "The options to modify the type of dice roll.", str, default='')
@lightbulb.command("roll", "Roll one or more dice.")
# Define the types of command that this function will implement
@lightbulb.implements(commands.SlashCommand)
async def dice(ctx: lightbulb.context.Context) -> None:
    # Extract the options from the context
    dice = ctx.options.dice
    options = ctx.options.options

    optionsList = ['a' in options, 'd' in options]
    if '1' in options:
        optionsList.append(1)
    if '2' in options:
        optionsList.append(2)
    
    if optionsList[0] and optionsList[1]:
        optionsList[0] = False
        optionsList[1] = False
    diceList = []
    bonusList = []

    try:
        diceList, bonusList = parseDice(dice)
    except ValueError as e:
        await ctx.respond("Invalid dice format.")
        return

    rolls, total = rollDice(diceList, bonusList, optionsList)

    response = f" {' + '.join([str(roll[0])+':'+str(roll[1]) for roll in rolls])}"
    if len(bonusList) > 0:
        response += f" + {' + '.join([str(bonus) for bonus in bonusList])}"

    response += f" = {total}"

    if len(response) > 2000:
        response = f"Dice body too long. Total roll: {total}."

    responseModifier = ""
    if optionsList[0]:
        responseModifier += " adv"
    elif optionsList[1]:
        responseModifier += " dis"
    
    for _ in optionsList:
        if type(_) == int:
            responseModifier += f" {_}s"
            


    response = f"Rolling {dice}{responseModifier}\n{response}"

    await ctx.respond(response)

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

# Pulls a number cards from a deck of cards
def pullCards(deck, number):
    cards = []
    if number > len(deck):
        raise ValueError("Not enough cards in deck.")
    for _ in range(number):
        cards.append(deck.pop())
    return cards


def load(bot: lightbulb.BotApp) -> None:
    bot.command(dice)
    bot.command(r20)
    bot.command(flip)
    bot.command(tarot)
    bot.command(deckofmany)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("dice"))
    bot.remove_command(bot.get_slash_command("r20"))
    bot.remove_command(bot.get_slash_command("flip"))
    bot.remove_command(bot.get_slash_command("tarot"))
    bot.remove_command(bot.get_slash_command("deckofmany"))

def parseDice(dice):
    diceList = []
    bonusList = []
    temp = ""
    digits = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
    whitespace = (" ", "\t", "\n")

    for char in dice:
        if char in whitespace:
            continue
        elif char == "-" and temp == "":
            temp += char
        elif char in digits:
            temp += char
        elif char == "d" and 'd' not in temp:
            temp += char
        elif char == "+" and temp != "" and 'd' not in temp:
            bonusList.append(int(temp))
            temp = ""
        elif char == '+' and temp != "" and 'd' in temp and temp[-1] != 'd':
            diceSplit = temp.split('d')
            if diceSplit[0] == "":
                diceSplit[0] = "1"
            diceList.append( (int(diceSplit[0]), int(diceSplit[1])) )
            temp = ""
        elif char == '-' and temp != "" and 'd' not in temp:
            bonusList.append(int(temp))
            temp = "-"
        elif char == '-' and temp != "" and 'd' in temp and temp[-1] != 'd':
            diceSplit = temp.split('d')
            if diceSplit[0] == "":
                diceSplit[0] = "1"
            diceList.append( (int(diceSplit[0]), int(diceSplit[1])) )
            temp = "-"
        else:
            # await ctx.respond("Invalid dice format.")
            raise ValueError("Invalid dice format.")
    
    if temp != "" and temp != "-":
        if "d" in temp and temp[-1] != "d":
            diceSplit = temp.split('d')
            if diceSplit[0] == "":
                diceSplit[0] = "1"
            diceList.append( (int(diceSplit[0]), int(diceSplit[1])) )
        elif "d" in temp and temp[-1] == "d":
            raise ValueError("Invalid dice format.")
        else:
            bonusList.append(int(temp))
        
    
    return diceList, bonusList

def rollDice(diceList, bonusList, optionsList=[]):
    rolls = []
    for dice in diceList:
        rollGroup = []
        for _ in range(abs(dice[0])):

            roll1 = random.randint(1, dice[1]) * int(dice[0] / abs(dice[0]))

            if optionsList[0] or optionsList[1]:
                roll2 = random.randint(1, dice[1]) * int(dice[0] / abs(dice[0]))

            if optionsList[0]:
                droll = max(roll1, roll2)
            elif optionsList[1]:
                droll =min (roll1, roll2)
            else:
                droll = roll1 

            if droll in optionsList:
                droll = random.randint(1, dice[1]) * int(dice[0] / abs(dice[0]))

            rollGroup.append(droll)
        rolls.append( ( f'{dice[0]}d{dice[1]}' , rollGroup) )
    
    total = sum([sum(roll[1]) for roll in rolls]) + sum(bonusList)
    return rolls, total


