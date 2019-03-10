import discord
from discord.utils import find, get
from discord.ext import commands
import asyncio
import random
import requests as rq
import json
import time




"""
PLEASE READ THROUGH THE CODE AS SOME OF THEM WILL REQUIRE YOU TO GET YOUR OWN API TOKEN OR DATABASE
The following commands/functions will require you to make some changes:
    update_notes
    weather
    define
    notes_db
"""



owm = '93c8becc18238c8fec19327ed6666655'


class Tools:
    def __init__(self, bot):
        self.bot = bot

    cms = commands.command(pass_context=True)




    @commands.command(pass_context=True)
    async def invite(self, con):
        """
        Function: Creates an invite link for the bot
        Command: `s.invite`
        Usage Example: `s.invite`
        """

        msg = discord.Embed(title="Discord Link: AMfDemh", url='https://discord.gg/AMfDemh',
                            description='Invite link for PZF (Pizza Bois)')
        await self.bot.send_message(con.message.channel, embed=msg)




    @commands.command(pass_context=True)
    async def weather(self, con):
        """
        Function: Check the weather of a certain city
        Command: `s.weather`
        Usage Example: `s.weather Mars` (Mars as in the city not planet)
        """

        session = rq.Session()
        city_state = con.message.content[10:]
        t = u"\u00b0"

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'.format(city_state, owm)
        r = session.get(url)
        rq_json = r.json()
        if r.status_code == 200:
            temp = rq_json['main']['temp']
            max_temp = rq_json['main']['temp_max']
            min_temp = rq_json['main']['temp_min']
            dis = rq_json['weather'][0]['description']
            wind = rq_json['wind']['speed']
            await self.bot.send_message(con.message.channel, "**Temperature** **in** **{}** **is around** {}{}F\n**Minimum Temperature is**: {}{}F\n**Maximum Temperature is**: {}{}F\n**Mainly**: {}\n**Wind speed is around**: {} **MPH**".format(city_state, temp, t, min_temp, t, max_temp, t, dis, wind))
        if r.status_code != 200:
            emb = discord.Embed(title='Error {}'.format(r.status_code))
            emb.set_image(url='https://http.cat/{}'.format(r.status_code))
            await self.bot.say(embed=emb)


    @commands.command(pass_context=True)
    async def pin(self, con, *, msg):
        """
        Function: Pins a message for you
        Command: `s.pin`
        Usage Example: `s.pin New Message!!`
        """

        await self.bot.pin_message(msg)


    



    @commands.command(pass_context=True, name='del')
    async def del_channel(self, con, *, name):
        """
        Function: Delete a channel
        Command: `s.del`
        Usage Example: `s.del general`
        """

        chan = find(lambda m: m.name == name, con.message.server.channels)
        await self.bot.delete_channel(chan)
        await self.bot.send_message(con.message.channel, "Channel {} has been deleted".format(name))

    


    @commands.command(pass_context=True, hidden=True)
    async def logout(self, con):
        """
        Function: Restarts the bot
        Command: `s.logout`
        Usage Example: `s.logout`
        """

        if con.message.author.id == '372737372154101763':
            await self.bot.send_message(con.message.channel, "Logging out bot now!")
            await self.bot.logout()
        else:
            await self.bot.send_message(con.message.channel, "I can't restart bot because you are not the creator or bot owner")

   



    @commands.command(pass_context=True)
    async def ping(self, con):
        """
        Function: Ping the bot?
        Command: `s.ping`
        Usage Example: `s.ping`
        """

        channel = con.message.channel
        t1 = time.perf_counter()
        await self.bot.send_typing(channel)
        t2 = time.perf_counter()
        embed = discord.Embed(title=None, description='Ping: {}'.format(
            round((t2-t1)*1000)), color=0x2874A6)
        await self.bot.send_message(con.message.channel, embed=embed)


    @commands.command(pass_context=True)
    async def channel(self, con, tpe, *, name):
        """
        Function: Create a channel
        Command: `s.channel`
        Usage Example: `s.channel voice Game Call` or `s.channel Game-text`
        """

        if tpe == 'text':
            tpe = discord.ChannelType.text
            if ' ' in name:
                name.replace(' ', '-')
            if '?' in name:
                name.replace('?', '')
                c_type = 'text'
        if tpe == 'voice':
            c_type = 'voice'
            tpe = discord.ChannelType.voice
        await self.bot.create_channel(con.message.server, name, type=tpe)
        await self.bot.send_message(con.message.channel, "**{}** channel **{}** created".format(c_type, name))



    @commands.command(pass_context=True)
    async def dice(self, con, min1=1, max1=6):
        """
        Function: Roll a dice with 1,6 numbers or give your own
        Command: `s.dice`
        Usage Example: `s.dice` or `s.dice 1 7` or `s.dice 4 7` (Notice there is a space)
        """
        r = random.randint(min1, max1)
        await self.bot.send_message(con.message.channel, "**{}**".format(r))




def setup(bot):
    bot.add_cog(Tools(bot))
