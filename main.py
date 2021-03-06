from discord.ext import commands # Bot Commands Frameworkをインポート
import os
import traceback # エラー表示のためにインポート
from cogs.observer import Observer

bot = commands.Bot(command_prefix='//')
bot.observe_channels = set()
bot.members = []
bot.rooms = []
bot.color = 0x9E7A7A
EXTENSIONS = [
    'cogs.observer',
    'cogs.shuffle',
    'cogs.enchant',
    'cogs.pin'
]

@bot.event
async def on_ready():
    guild = bot.get_guild(int(os.environ["GUILD_ID"]))
    print('-------------------')
    print('ready:' + guild.name)
    print('-------------------')
    # os.system(f'curl -XPOST -d "token={os.environ["SLACK_TOKEN"]}" -d "channel=#{os.environ["SLACK_CHANNEL"]}" -d "text=densan botが起動しました。" "https://slack.com/api/chat.postMessage"')


    ch1 = guild.get_channel(753978604051890207)
    bot.observe_channels.add(ch1)
    ch2 = guild.get_channel(753978640806445107)
    bot.observe_channels.add(ch2)
    ch3 = guild.get_channel(755235384744607856)
    bot.observe_channels.add(ch3)

for extension in EXTENSIONS:
    bot.load_extension(extension)

bot.run(os.environ["DISCORD_TOKEN"])
