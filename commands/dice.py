import random
import lightbulb
from lightbulb import commands


# These two are the same type, but are optional. We can provide a
# default value simply by using the `default` kwarg.
@lightbulb.option("dice", "The dice to be rolled, will roll a single d20 if no value provided.", str, default='1d20')

@lightbulb.command("roll", "Roll one or more dice.")
# Define the types of command that this function will implement
@lightbulb.implements(commands.SlashCommand)
async def dice(ctx: lightbulb.context.Context) -> None:
    # Extract the options from the context
    dice = ctx.options.dice
    
    diceList = []
    bonusList = []

    try:
        diceList, bonusList = parseDice(dice)
    except ValueError as e:
        await ctx.respond("Invalid dice format.")

    rolls, total = rollDice(diceList, bonusList)

    response = f" {' + '.join([str(roll[0])+':'+str(roll[1]) for roll in rolls])}"
    if len(bonusList) > 0:
        response += f" + {' + '.join([str(bonus) for bonus in bonusList])}"

    response += f" = {total}"

    if len(response) > 2000:
        response = f"Dice body too long. Total roll: {total}."

    await ctx.respond(response)

def load(bot: lightbulb.BotApp) -> None:
    bot.command(dice)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("dice"))

def parseDice(dice):
    diceList = []
    bonusList = []
    temp = ""
    digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    whitespace = [" ", "\t", "\n"]

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

def rollDice(diceList, bonusList):
    rolls = []
    for dice in diceList:
        rollGroup = []
        for _ in range(abs(dice[0])):
            rollGroup.append( random.randint(1, dice[1]) * int(dice[0] / abs(dice[0])) )
        rolls.append( ( f'{dice[0]}d{dice[1]}' , rollGroup) )
    
    total = sum([sum(roll[1]) for roll in rolls]) + sum(bonusList)
    return rolls, total