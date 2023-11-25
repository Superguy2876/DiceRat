import random
from urllib import response
import lightbulb
import hikari
import os
from lightbulb import commands
import redis
from dyce import H
from ..dice import DicePool, Dice
import asyncio



@lightbulb.command("test", "test command")
@lightbulb.implements(commands.SlashCommand)
async def test(ctx: lightbulb.context.Context) -> None:
    
    await ctx.respond("test")


@lightbulb.command("valuetest", "test command")
@lightbulb.implements(commands.SlashCommand)
async def valuetest(ctx: lightbulb.context.Context) -> None:
    # we get some dice and roll them all, counting the outcomes, all dice will be d20s
    dice = DicePool('1000d20')
    


# command to test attaching a txt file to a message
@lightbulb.command("testfile", "test command")
@lightbulb.implements(commands.SlashCommand)
async def testfile(ctx: lightbulb.context.Context) -> None:
    # create file
    f = open("test.txt", "w")
    f.write("test")
    f.close()

    # get the file as a hikari.File
    file = hikari.File("test.txt")
    # send file
    await ctx.respond('test', attachment=file)

    # delete file
    os.remove("test.txt")



@lightbulb.command("test_wait", "test command")
@lightbulb.implements(commands.SlashCommand)
async def test_wait(ctx: lightbulb.context.Context) -> None:
    # Send initial response
    initial_response = await ctx.respond("Beginning test")

    # Wait for 5 seconds
    await asyncio.sleep(5)

    # Edit the message
    await ctx.edit_last_response("Finished test")


def load(bot: lightbulb.BotApp) -> None:
    bot.command(test)
    bot.command(test_wait)
    bot.command(testfile)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("test"))
    bot.remove_command(bot.get_slash_command("test_wait"))
    bot.remove_command(bot.get_slash_command("testfile"))