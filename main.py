from discord.ext import commands # Bot Commands Frameworkをインポート
import os
import traceback # エラー表示のためにインポート
from cogs.observer import Observer

bot = commands.Bot(command_prefix='!!')
bot.observe_channels = set()
EXTENSIONS = [
    'cogs.observer'
]

@bot.event
async def on_ready():
    print('-----')
    print('ready')
    print('-----')

for extension in EXTENSIONS:
    bot.load_extension(extension)

bot.run(os.environ["DISCORD_TOKEN_DEV"])
