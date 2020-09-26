from discord.ext import commands # Bot Commands Frameworkをインポート
import os
import traceback # エラー表示のためにインポート
from cogs.observer import Observer

bot = commands.Bot(command_prefix='/')
bot.observe_channels = set()
bot.members = []
bot.rooms = []
EXTENSIONS = [
    'cogs.observer',
    'cogs.shuffle'
]

@bot.event
async def on_ready():
    print('-----')
    print('ready')
    print('-----')
    os.system(f'curl -XPOST -d "token={os.environ["SLACK_TOKEN"]}" -d "channel=#{os.environ["SLACK_CHANNEL"]}" -d "text=densan botが起動しました。" "https://slack.com/api/chat.postMessage"')

for extension in EXTENSIONS:
    bot.load_extension(extension)

bot.run(os.environ["DISCORD_TOKEN"])
