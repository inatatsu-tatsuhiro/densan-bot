from discord.ext import commands, tasks

import discord
import re

class Enchant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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

    @commands.command()
    async def create_role(self, ctx, role_name):
        role = await ctx.guild.create_role(name=role_name)
        if not role == None:
            await ctx.send(f'{role.mention}を作成しました。')


    
    @commands.Cog.listener(name='on_reaction_add')
    async def on_reaction_add(self, reaction, user):
        if reaction.message.content.startswith('*'):
            await user.add_roles(reaction.message.role_mentions[0])

def setup(bot):
    bot.add_cog(Enchant(bot))