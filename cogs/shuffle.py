from discord.ext import commands, tasks

import discord
import random
import time

class Shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sh'])
    async def shuffle_help(self, ctx):
        f = open('./cogs/help/shuffle.txt')
        lines = f.readlines()
        f.close()
        discription = ""
        for l in lines:
            discription += l
        em = discord.Embed(title="Shuffle Help", description=discription, colour=self.bot.color)
        await ctx.send(embed=em)


    @commands.command(aliases=['crm'])
    async def create_room(self, ctx, category_id, num):
        ch = ctx.guild.get_channel(int(category_id))
        if ch in ctx.guild.categories:
            for i in range(int(num)):
                tc = await ctx.guild.create_text_channel('room'+str(i+1))
                vc = await ctx.guild.create_voice_channel('room'+str(i+1))
                await vc.edit(category=ch)
                await tc.edit(category=ch)
                self.bot.rooms.append(vc)
                self.bot.rooms.append(tc)
        else:
            await ctx.send('カテゴリが見つかりません。')

    @commands.command(aliases=['rt'])
    async def room_timer(self, ctx, m):
        self.bot.timer = int(m)*60
        await ctx.send('タイマーを'+m+'分でセットしました。')

    @tasks.loop(minutes=1.0)
    async def time_keep(self, ctx):
        if(self.bot.timer + self.bot.start_time <= int(time.time()) and self.bot.flag):
            self.bot.flag = False
            await ctx.send('終了です。')
            for mem in self.bot.members:
                await mem.move_to(channel=self.bot.here)
                await mem.edit(mute=True)
            for room in self.bot.rooms:
                await room.delete()
            self.bot.rooms.clear()
            self.time_keep.cancel()
        elif(self.bot.flag):
            remain = int((self.bot.timer + self.bot.start_time) - time.time())
            await ctx.send('残り'+str((remain // 60)+1)+'分' )


    @commands.command()
    async def mute(self, ctx):
        await ctx.author.edit(mute=True)
    @commands.command()
    async def unmute(self, ctx):
        await ctx.author.edit(mute=False)
    
    @commands.command(aliases=['s'])
    async def shuffle(self, ctx):
        self.bot.members = [mem for mem in ctx.author.voice.channel.members if not ctx.author == mem]
        random.shuffle(self.bot.members)
        self.bot.here = ctx.author.voice.channel
        i = 0
        for mem in self.bot.members:
            await mem.move_to(channel=self.bot.rooms[i])
            await mem.adit(mute=False)
            i += 1
            if len(self.bot.rooms) <= i:
                i = 0
        self.bot.start_time = int(time.time())
        self.bot.flag = True
        self.time_keep.start(ctx)
        await ctx.send('ルーム分け完了しました。ルームの時間は'+str(self.bot.timer // 60)+'分です。')

    
    
def setup(bot):
    bot.add_cog(Shuffle(bot))