import os
from dotenv import dotenv_values
import hikari
import lightbulb

import DiceRat


def create_bot() -> lightbulb.BotApp:
    # Load the token from a secrets file you'll need to create yourself.
    config = dotenv_values('./DiceRat/.env')
    print(' '.join(config.keys()))
    DISCORD_TOKEN = config['DISCORD_TOKEN']
    # Create the main bot instance with all intents.
    bot = lightbulb.BotApp(
        token=DISCORD_TOKEN,
        prefix="!",
        intents=8,
        default_enabled_guilds=DiceRat.GUILD_ID,
    )

    # Load all extensions.
    bot.load_extensions_from("./DiceRat/commands")
    command_list = bot.slash_commands
    for command in command_list:
        print(command)
        print('\n'.join(dir(command_list[command])))
    print(command_list)

    return bot


if __name__ == "__main__":
    if os.name != "nt":
        # uvloop is only available on UNIX systems, but instead of
        # coding for the OS, we include this if statement to make life
        # easier.
        import uvloop

        uvloop.install()

    # Create and run the bot.
    create_bot().run()