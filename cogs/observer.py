from discord.ext import commands, tasks

import discord
import os

class Observer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, channel_id: str):
        flag = False
        ch = ctx.guild.get_channel(int(channel_id))
        if ch in ctx.bot.observe_channels:
            ch = ctx.guild.get_channel(int(channel_id))
            await ctx.send(ch.name + 'は追加済みです。')
            return
        for ch in ctx.guild.voice_channels:
            if str(ch.id) == channel_id:
                flag = True
        if flag:
            ch = ctx.guild.get_channel(int(channel_id))
            ctx.bot.observe_channels.add(ch)
            await ctx.send(ch.name + 'を追加しました。')
        else:
            await ctx.send(channel_id + 'に該当するVoice Channelはありません。')

    @commands.command()
    async def list(self, ctx):
        msg = "========部室(VC)一覧========\n"
        for ch in ctx.bot.observe_channels:
            msg += (ch.name + "\n")
        msg += "=========================="
        await ctx.send(msg)
    
    @commands.command()
    async def remove(self, ctx, channel_id: str):
        ch = ctx.guild.get_channel(int(channel_id))
        if ch in ctx.bot.observe_channels:
            ctx.bot.observe_channels.remove(ch)
            await ctx.send(ch.name + 'を削除しました。')



    @commands.Cog.listener(name='on_voice_state_update')
    async def on_voice_state_update(self, member, before, after):
        if before.channel is not after.channel and after.channel in self.bot.observe_channels and len(after.channel.members) == 1:
            msg = f'{member.display_name}が{after.channel.name}を開室しました。'
            await self.nortificate(msg)
           
        if before.channel is not after.channel and before.channel in self.bot.observe_channels and len(before.channel.members) == 0:
            msg = f'{member.display_name}が{before.channel.name}を閉室しました。'
            await self.nortificate(msg)

    async def nortificate(self, msg):
        os.system(f'curl -XPOST -d "token={os.environ["SLACK_TOKEN"]}" -d "channel=#{os.environ["SLACK_CHANNEL"]}" -d "text={msg}" "https://slack.com/api/chat.postMessage"')
    
def setup(bot):
    bot.add_cog(Observer(bot))