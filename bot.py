import discord
from discord.ext import commands
import asyncio
import requests as rq
import json
import random
from itertools import cycle

extensions=['fun','tools']

TOKEN = 'NTUwMDI5NDY4ODE5OTE0NzUy.D15QTw.TmGVfNy6KQQ_eaLIOOuLtSd1kVk'

bot = commands.Bot(command_prefix = '.')
bot.remove_command('help')


async def cycling_status():
    watching_list = ['The Great Pizza War', 'You', 'World War VII','The Retro Era', 'Abominable','PewDiePie']
    games = ['.h | Help Commands','.help | Help Commands','Club Penguin Rewritten', 'Pizzatron', 'Spraying sauce']
    listening_list = ['Tactics','IN CHEESE WE PLEASE','.h for help','U']
    
    
    while True:
        num = random.choice([1, 2, 3])
        sleepTime = random.choice([3000, 2000, 1000, 1500, 2500, 500, 1234, 400, 200, 580, 800])
        if num == 1:
            await bot.change_presence(game=discord.Game(name=random.choice(games), type=1))
        if num == 2:
            await bot.change_presence(game=discord.Game(name=random.choice(listening_list), type=2))
        if num == 3:
            await bot.change_presence(game=discord.Game(name=random.choice(watching_list), type=3))
        await asyncio.sleep(sleepTime)


@bot.event
async def on_ready():
    await cycling_status()
    print("Change status for {} is ready!".format(bot.user.name))





for extension in extensions:
    try:
        bot.load_extension(extension)
        print("{} loaded".format(extension))
    except Exception as error:
        print("Unable to load extension {} error {}".format(extension, error))


@bot.command()
async def marco():
    await bot.say('Polo!')


@bot.command(pass_context=True)
async def userinfo(ctx, member: discord.Member = None):
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=member.colour, timestamp=ctx.message.timestamp)
    embed.set_author(name=member)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)
    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)
    await bot.send_message(ctx.message.channel,embed=embed)

@bot.command(pass_context=True)
async def online(con):
    amt = 0
    for i in con.message.server.members:
        if i.status != discord.Status.offline:
            amt += 1
    await bot.send_message(con.message.channel, "**Currently `{}` Members Online In `{}`**".format(amt,con.message.server.name))



@bot.command(pass_context=True)
async def offline(con):
    amt = 0
    for i in con.message.server.members:
        if i.status == discord.Status.offline:
            amt += 1
    await bot.send_message(con.message.channel, "**Currently `{}` Members Offline In `{}`**".format(amt,con.message.server.name))


@bot.event
async def on_command_error(con,error):
    if error.message.content.startswith('.kick') or error.message.content.startswith(".ban"):
        await bot.send_message(error.message.channel,"**Mentioned user is not found**")


@bot.command(pass_context=True)
async def kick(con,user:discord.Member=None):
    if con.message.author.server_permissions.kick_members == True or con.message.author.server_permissions.administrator == True:
        await bot.kick(user)
        await bot.send_message(con.message.channel,"User {} has been kicked".format(user.name))
    else:
        await bot.send_message(con.message.channel, "**Insufficient Permissions To Kick Member**")

@bot.command(pass_context=True)
async def ban(con,user:discord.Member):
    if con.message.author.server_permissions.ban_members == True or con.message.author.server_permissions.administrator == True:
        await bot.ban(user)
        await bot.send_message(con.message.channel, "User {} has been banned".format(user.name))
    else:
        await bot.send_message(con.message.channel, "**Insufficient Permissions To Ban Member**")



@bot.command(pass_context=True)
async def urban(con, *, msg):
        rq_json = rq.Session().get('http://api.urbandictionary.com/v0/define?term={}'.format(msg)).json()
        if rq_json['list'] == []:
            await bot.say("**No Results Found**")
        elif rq_json['list'] != []:
            #await client.send_message(con.message.channel, "**Word**: {}\n**Votes**: {}\n**Definitioin**: {}\n**Example**: {}".format(rq_json['list'][0]['word'], rq_json['list'][0]['thumbs_up'], rq_json['list'][0]['definition'], rq_json['list'][0]['example']))
            ur="**Word: ``{}``**\n**Votes:** {}\n**Definitioin:** {}\n**Example:** {}".format(rq_json['list'][0]['word'], rq_json['list'][0]['thumbs_up'], rq_json['list'][0]['definition'], rq_json['list'][0]['example'])
            emb=discord.Embed(description=ur,colour=con.message.author.colour)
            await bot.say(embed=emb)



@bot.command(pass_context=True)
async def ball8(ctx,*,question=None):
        if question == None:
            await bot.say("Please ask a question")

        if question != None:
            embed = discord.Embed(
                title ='',
                description = "{}".format(ctx.message.author),
                colour=ctx.message.author.colour,
            )
            embed.set_footer(text="")
            embed.set_image(url='')
            embed.set_thumbnail(url='')
            embed.add_field(name= ":question:Question:", value='{}'.format(ctx.message.content[6:]), inline=False)
            embed.add_field(name= ":8ball:8ball", value='{}'.format(random.choice(['Yes','No', 'It is certain','It is decidedly so', 'Without a doubt',
                        'Yes, definitely', 'You may rely on it', 'As I see it, yes',
                            'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                            'Reply hazy try again', 'Ask again later',
                            'Better not tell you now', 'Cannot predict now',
                            'Concentrate and ask again', 'Dont count on it',
                            'My reply is no', 'My sources say no',
                            'Outlook not so good', 'Very doubtful'])), inline=True)
            await bot.say(embed=embed)




@bot.command(pass_context=True)
async def dog(con):
        r = rq.Session().get('https://random.dog/woof.json').json()
        emb = discord.Embed(title='Dog')
        emb.set_image(url=r['url'])
        await bot.send_message(con.message.channel, embed=emb)


@bot.command(pass_context=True)
async def help (ctx):
    em=discord.Embed(colour=0x68f724,title="My prefix is **.** ``.``",description="")
    await bot.send_message(ctx.message.author, embed=em)
    embed=discord.Embed(colour=0x68f724,title="Default Commands:",description="")
    embed.add_field(name=".help/.h", value="Displays this menu.", inline=False)
    embed.add_field(name=".8ball <question>", value="Tells you the answer to your question.", inline=False)
    embed.add_field(name=".userinfo <@user>", value="Gets information about a mentioned user", inline=False)
    embed.add_field(name=".online", value="Checks how many users are online.", inline=False)
    embed.add_field(name=".offline", value="Checks how many users are offline.", inline=False)
    embed.add_field(name=".channel <.channel voice Game Call` or `s.channel Game-text>", value="Creates a text or voice channel.", inline=False)
    embed.add_field(name=".del <channel name>", value="Deletes a text or voice channel.", inline=False)
    embed.add_field(name=".pin <message>", value="Pins a message for you", inline=False)
    embed.add_field(name=".dice <dice` or `s.dice 1 7` or `s.dice 4 7` (Notice there is a space)>", value="Roll a dice with 1,6 numbers or give your own", inline=False)
    embed.add_field(name=".weather <city name> Check the weather of a certain city", value="Roll a dice with 1,6 numbers or give your own", inline=False)
    embed.add_field(name=".invite", value="Creates an invite link for this server", inline=False)
    embed.add_field(name=".randomshow>", value="The name is self explanatory.", inline=False)
    embed.add_field(name=".catfact", value="Gets facts about cats, cos y not?", inline=False)
    embed.add_field(name=".randomanime", value="This name is self explanatory.", inline=False)
    embed.add_field(name=".randommovie", value="This name is also self explanatory.", inline=False)
    embed.add_field(name=".cat", value="Random cat pictures", inline=False)
    embed.add_field(name=".dog", value="Random dog pictures.", inline=False)
    embed.add_field(name=".urban <word>", value="Searches the urban dictionary.", inline=False)
    embed.add_field(name=".cookie <`@username`>", value="Gives user cookies", inline=False)
    embed.add_field(name=".bunnyfact", value="Random bunny facts.", inline=False)
    embed.add_field(name=".pifact", value="Random facts about pi", inline=False)
    embed.add_field(name=".dogfact", value="Random dog facts", inline=False)
    embed.add_field(name=".game <whatever you want", value="Changes the bot's playing status", inline=False)
    embed.add_field(name=".listening", value="Changes the bot's listening status", inline=False)
    embed.add_field(name=".watching", value="Changes the bot's watching status", inline=False)
    embed.add_field(name=".bunny", value="random pictures of bunnies, cos y not?", inline=False)
    await bot.send_message(ctx.message.author, embed=embed)
    e=discord.Embed(colour=0x68f724,title=" :white_check_mark:  **Sucess!**",description="I've sent you a list of commands in your **Direct Messages**!")
    await bot.send_message(ctx.message.channel, embed=e)




@bot.command(pass_context=True)
async def h (ctx):
    em=discord.Embed(colour=0x68f724,title="My prefix is **.** ``.``",description="")
    await bot.send_message(ctx.message.author, embed=em)
    embed=discord.Embed(colour=0x68f724,title="Default Commands:",description="")
    embed.add_field(name=".help", value="Displays this menu.", inline=False)
    embed.add_field(name=".8ball <question>", value="Tells you the answer to your question.", inline=False)
    embed.add_field(name=".userinfo <@user>", value="Gets information about a mentioned user", inline=False)
    embed.add_field(name=".online", value="Checks how many users are online.", inline=False)
    await bot.send_message(ctx.message.author, embed=embed)
    e=discord.Embed(colour=0x68f724,title=" :white_check_mark:  **Success!**",description="I've sent you a list of my commands in your **Direct Messages**")
    await bot.send_message(ctx.message.channel, embed=e)


bot.run(TOKEN)
