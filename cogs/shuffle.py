from discord.ext import commands, tasks

import discord
import random
import time

class Shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx, category_id, num):
        ch = ctx.guild.get_channel(int(category_id))
        if ch in ctx.guild.categories:
            for i in range(int(num)):
                vc = await ctx.guild.create_voice_channel('room'+str(i+1))
                await vc.edit(category=ch)
                self.bot.rooms.append(vc)
        else:
            await ctx.send('そんなカテゴリねーよ')

    @commands.command()
    async def timer(self, ctx, m):
        self.bot.timer = int(m)*60
        await ctx.send('タイマーを'+m+'分でセットしました。')

    @tasks.loop(minutes=1.0)
    async def time_keep(self, ctx):
        if(self.bot.timer + self.bot.start_time <= int(time.time()) and self.bot.flag):
            self.bot.flag = False
            await ctx.send('終了です。')
            for mem in self.bot.members:
                await mem.move_to(channel=self.bot.here)
            for room in self.bot.rooms:
                await room.delete()
            self.bot.rooms.clear()
            self.time_keep.cancel()
        elif(self.bot.flag):
            remain = int((self.bot.timer + self.bot.start_time) - time.time())
            await ctx.send('残り'+str((remain // 60)+1)+'分' )




    @commands.command()
    async def shuffle(self, ctx):
        self.bot.members = [mem for mem in ctx.author.voice.channel.members if not ctx.author == mem]
        random.shuffle(self.bot.members)
        self.bot.here = ctx.author.voice.channel
        i = 0
        for mem in self.bot.members:
            await mem.move_to(channel=self.bot.rooms[i])
            i += 1
            if len(self.bot.rooms) <= i:
                i = 0
        self.bot.start_time = int(time.time())
        self.bot.flag = True
        self.time_keep.start(ctx)
        await ctx.send('ルーム分け完了しました。ルームの時間は'+str(self.bot.timer // 60)+'分です。')

    @commands.command()
    async def test(self, ctx):
        self.bot.start_time = int(time.time())
        self.bot.flag = True
        self.time_keep.start(ctx)
        await ctx.send('time_keep start' + str(self.bot.start_time))


    
    
def setup(bot):
    bot.add_cog(Shuffle(bot))