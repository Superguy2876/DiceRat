import random
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

    response = f"Rolling {dice}\n{response}"

    await ctx.respond(response)

@lightbulb.option("modifier", "The modifier to be added to the roll.", int, default=0)
@lightbulb.option("options", "The options to modify the type of dice roll.", str, default='')
@lightbulb.command("r20", "Roll a d20 with modifiers.")
@lightbulb.implements(commands.SlashCommand)
async def r20(ctx: lightbulb.context.Context) -> None:
    modifier = ctx.options.modifier
    options = ctx.options.options

    optionsList = ['a' in options, 'd' in options]
    if '1' in options:
        optionsList.append(1)

    rolls, total = rollDice([(1, 20)], [modifier], optionsList)

    response = f" {' + '.join([str(roll[0])+':'+str(roll[1]) for roll in rolls])}"
    if len(bonusList) > 0:
        response += f" + {' + '.join([str(bonus) for bonus in bonusList])}"

    response += f" = {total}"

    if len(response) > 2000:
        response = f"Dice body too long. Total roll: {total}."

    response = f"Rolling 1d20\n{response}"

    await ctx.respond(response)

def load(bot: lightbulb.BotApp) -> None:
    bot.command(dice)
    bot.command(r20)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("dice"))
    bot.remove_command(bot.get_slash_command("r20"))

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