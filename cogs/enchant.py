from discord.ext import commands, tasks

import discord
import re
import os

class Enchant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['eh'])
    async def enchant_help(self, ctx):
        f = open('./cogs/help/enchant.txt')
        lines = f.readlines()
        f.close()
        discription = ""
        for l in lines:
            discription += l
        em = discord.Embed(title="Enchant Help", description=discription, colour=self.bot.color)
        await ctx.send(embed=em)

    @commands.command(aliases=['er'])
    async def enchant_role(self, ctx, role_mention):
        flag = False        
        for r in ctx.guild.roles:
            if r.mention == role_mention:
                flag = True
                role = r
        if flag:
            await ctx.send(f'*リアクションを付けると{role.mention}を付与します。')
        else:
            await ctx.send('404')

    @commands.command(aliases=['crl'])
    async def create_role(self, ctx, role_name):
        role = await ctx.guild.create_role(name=role_name)
        if not role == None:
            await ctx.send(f'{role.mention}を作成しました。')

    @commands.command(aliases=['rr'])
    async def release_role(self, ctx, role_name):
        flag = False
        r = None
        if role_name.startswith('<@&'):
            r_name = ctx.guild.get_role(int(role_name[3:-1])).name
        else:
            r_name = role_name
        for role in ctx.guild.roles:
            if r_name == role.name:
                flag = True
                r = role

        if flag:
            await ctx.author.remove_roles(r)
            await ctx.send(f'ロール:{r_name}を解除しました。')
        else:
            await ctx.send(f'ロール{r_name}は見つかりません。')


    
    @commands.Cog.listener(name='on_raw_reaction_add')
    async def on_raw_reaction_add(self, payload):
        ch = self.bot.get_channel(payload.channel_id)
        msg = await ch.fetch_message(payload.message_id)
        mem = payload.member
        
        if msg.content.startswith('*') and msg.author.bot:
            await mem.add_roles(msg.role_mentions[0])

def setup(bot):
    bot.add_cog(Enchant(bot))