import random
import re
import lightbulb
from lightbulb import commands


# These two are the same type, but are optional. We can provide a
# default value simply by using the `default` kwarg.
@lightbulb.option("dice", "A fixed number to add to the total roll.", str, default='1d20')

@lightbulb.command("roll", "Roll one or more dice.")
# Define the types of command that this function will implement
@lightbulb.implements(commands.SlashCommand)
async def dice(ctx: lightbulb.context.Context) -> None:
    # Extract the options from the context
    dice = ctx.options.dice
    
    diceList = re.findall(r'(-?\s*\d+)(d\d+)|(-?\s*\d+)|(d\d+)', dice)
    print(diceList)

    

    # rolls = [random.randint(1, sides) for _ in range(number)]

    # To send a message, use ctx.respond. Using kwargs, you can make the
    # bot reply to a message (when not sent from a slash command
    # invocation), allow mentions, make the message ephemeral, etc.
    # await ctx.respond(
    #     " + ".join(f"{r}" for r in rolls)
    #     + (f" + {bonus} (bonus)" if bonus else "")
    #     + f" = **{sum(rolls) + bonus:,}**"
    # )

    await ctx.respond('test')


def load(bot: lightbulb.BotApp) -> None:
    bot.command(dice)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("dice"))