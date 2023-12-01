import os
from dotenv import dotenv_values
import hikari
import lightbulb
import redis

class RatBotApp(lightbulb.BotApp):
    def __init__(self, redis_pool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_pool = redis_pool

def create_bot() -> lightbulb.BotApp:
    # Load the token from a secrets file you'll need to create yourself.
    config = dotenv_values('.env')
    print(' '.join(config.keys()))
    DISCORD_TOKEN = config['DISCORD_TOKEN']
    GUILD_IDs = list(map(int, config['GUILD_IDs'].split(', ')))
    print(type(GUILD_IDs))

    pool = redis.ConnectionPool(host='redis', port=6379, db=0, decode_responses=True)
    

    print(GUILD_IDs)
    # Create the main bot instance with all intents.
    bot = RatBotApp(
        redis_pool=pool,
        token=DISCORD_TOKEN,
        prefix="!",
        intents=8,
        default_enabled_guilds=GUILD_IDs,
    )

    

    # Load all extensions.
    bot.load_extensions_from("./src/commands")
    command_list = bot.slash_commands
    for command in command_list:
        print(command)
        
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