from dotenv import dotenv_values
import hikari
config = dotenv_values('.env')

DISCORD_TOKEN = config['DISCORD_TOKEN']
bot = hikari.GatewayBot(DISCORD_TOKEN)

@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)

@bot.listen(hikari.GuildJoinEvent)
@bot.listen(hikari.StartedEvent)
async def on_start(event):
    print('RAT HAS ARRIVED!')

bot.run()