from discord.ext import commands, tasks

import discord

class Pin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ph'])
    async def pin_help(self, ctx):
        f = open('./cogs/help/pin.txt')
        lines = f.readlines()
        f.close()
        discription = ""
        for l in lines:
            discription += l
        em = discord.Embed(title="Pin Help", description=discription, colour=self.bot.color)
        await ctx.send(embed=em)

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def on_raw_reaction_add(self, payload):
        print('add:' + payload.emoji)
        if not(payload.emoji.name == '📌'):
            return
        ch = self.bot.get_channel(payload.channel_id)
        msg = await ch.fetch_message(payload.message_id)
        await msg.pin()
    @commands.Cog.listener(name='on_raw_reaction_remove')
    async def on_raw_reaction_remove(self, payload):
        print('delete: ' + payload.emoji)
        if not(payload.emoji.name == '📌'):
            return
        ch = self.bot.get_channel(payload.channel_id)
        msg = await ch.fetch_message(payload.message_id)
        pins = await ch.pins()
        if not(msg in pins):
            return

        await msg.unpin()
        await ch.send('ピンを外しました')
        


    
    
def setup(bot):
    bot.add_cog(Pin(bot))