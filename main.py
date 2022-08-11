import os
import discord
from discord.ext import commands
from def_list import *
from my_list import *
from music import Player
from tinydb import TinyDB, Query

client = commands.Bot(command_prefix='.',
                      intents=discord.Intents.all(), help_command=None)

db = TinyDB('db.json')
User = Query()

# <editor-fold desc="client event">


@client.event
async def on_ready():
    print('{0.user} vừa du hành vào sever'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Đời | .help'))


@client.event
async def on_member_join(member):
    print(f'{member} vừa du hành vào sever')


@client.event
async def on_member_out(member):
    print(f'{member} vừa bay màu khỏi sever')


# </editor-fold>


# <editor-fold desc="All Command...">
# <editor-fold desc="help">
@client.command()
async def help(ctx, sub=None):
    await ctx.message.add_reaction('👍')
    if sub == None or sub == '0':
        await ctx.send('Danh sách những gì hiện có:')
        for i in range(len(shelp)):
            await ctx.send(f'{i + 1}: {shelp[i]}')
        await ctx.send('Chi tiết: .help [stt] - VD: .help 1')

    elif cint(sub) == False:
        await ctx.send(cero())
        return

    else:
        await ctx.send(dhelp[int(sub) - 1])
# </editor-fold>


# <editor-fold desc="activity">
@client.command(name='activity')
async def activities(ctx, name='free', *, sub='...'):
    x = f'{sub} | .help'
    if name == 'free':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.unknown))
    elif name == 'watch':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=x))
    elif name == 'play':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=x))
    elif name == 'stream':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=x))
    elif name == 'listen':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=x))
    else:
        pass
# </editor-fold>


# <editor-fold desc="ping">
@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
@client.command()
async def ping(ctx):
    await ctx.message.add_reaction('💥')
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
# </editor-fold>


# <editor-fold desc="clear">
@client.command()
async def clear(ctx, n=1):
    await ctx.channel.purge(limit=n + 1)
# </editor-fold>


# <editor-fold desc="quote">
@client.command()
async def quote(ctx):
    await ctx.message.add_reaction('🆗')
    quote = get_quote()
    await ctx.send(quote)
# </editor-fold>


# <editor-fold desc="lovegame">
@client.command()
async def lovegame(ctx, f=None, m=None):
    try:
        await ctx.message.add_reaction('💕')
        love = love_calculater(f, m)
        await ctx.send(love)
    except:
        await ctx.send('.lovegame [name 1] [name 2]')
# </editor-fold>


# <editor-fold desc="numgame">
@client.command()
async def numgame(ctx):
    await ctx.message.add_reaction('🔢')
    number = random.randint(1, 100)
    await ctx.send('\tĐoán số trong khoảng 1 - 100\nBạn có 7 lượt\n' + '-' * 20)
    for guess in reversed(range(7)):
        await ctx.send(f'{guess + 1} lượt còn lại...\nNhập số: ')
        message = await client.wait_for('message')
        msg = message.content
        if cint(msg) == False:
            await ctx.send('Lỗi!!! Game dừng lại\nNhập éo gì v, chắc chắn ko phải số')
            break
        attempt = int(msg)
        if attempt > number:
            await ctx.send('Bé hơn số vừa chọn\n' + '-' * 10)
        elif attempt < number:
            await ctx.send('Lớn hơn số vừa chọn\n' + '-' * 10)
        else:
            await ctx.send('Chúc mừng!\nKhÓ vẬy cũng làm đc :)')
            break
    else:
        await ctx.send("Gà! Bạn đã hết lượt chơi")
# </editor-fold>


# <editor-fold desc="rannum">
@client.command()
async def rannum(ctx, min=None, max=None):
    await ctx.message.add_reaction('💯')

    def check(x):
        try:
            test = int(x)
            return True
        except:
            return False

    if min == None and max == None:
        await ctx.send(random.randint(1, 100))

    elif check(min) == True and check(max) == True:
        await ctx.send(random.randint(int(min), int(max)))

    elif check(min) == True and max == None:
        await ctx.send(random.randint(1, int(min)))

    else:
        await ctx.send(cero())
# </editor-fold>


# <editor-fold desc="hiujoke">
@client.command()
async def hiujoke(ctx):
    await ctx.message.add_reaction('🆗')
    await ctx.send(hiujokes())
    return
# </editor-fold>


# <editor-fold desc="avatar">
@client.command()
async def avatar(ctx, *, avamember: discord.Member = None):
    try:
        await ctx.send(avamember.avatar_url)
    except:
        await ctx.send(ctx.author.avatar_url)
# </editor-fold>


@client.command()
async def isert(ctx, *, sentence):
    s = sentence.split('/')[0].lower()
    d = sentence.split('/')[1]
    try:
        db.insert({'s': s, 'd': d})
        await ctx.send('Đã thêm thành công')
    except:
        await ctx.send('.isert a/b')


@client.command()
async def rmove(ctx, *, sentence):
    s = sentence.split('/')[0].lower()
    d = sentence.split('/')[1]
    if d == 'all':
        db.remove(User.s == s)/all
    try:
        db.remove((User.s == s) & (User.d == d))
        await ctx.send('Đã xóa thành công')
    except:
        await ctx.send('.rmove a/b hoặc câu không tồn tại')


@client.command()
async def lall(ctx):
    embed = discord.Embed(title='Danh sách', colour=ctx.author.colour)
    for item in db:
        embed.add_field(name='\u200b', value=f'`{item["s"]}`: {item["d"]}')
    await ctx.send(embed=embed)

# </editor-fold>


@client.listen()
async def on_message(message):
    if message.author == client.user:
        return

    # <editor-fold desc="Variable">
    msg = message.content
    msc = message.channel
    msgl = message.content.lower()
    # </editor-fold>

    try:
        if msg.startswith(msg):
            await msc.send(random.choice(db.search(User.s == msgl))['d'])
    except:
        pass

    # nói đạo lý
    if any(word in msgl for word in ['nói']):
        if any(word in msgl for word in ['đạo lý']):
            await message.add_reaction('🆗')
            quote = get_quote()
            await msc.send(quote)
            return

    # nói joke
    if any(word in msgl for word in ['nói']):
        if any(word in msgl for word in ['joke']):
            await message.add_reaction('🆗')
            await msc.send(hiujokes())
            return

    # chí tử
    if any(word in msgl for word in ['chí tử']):
        await message.add_reaction('🔥')
        await msc.send('Chí tử cc')
        return

    # lời chào
    if any(word in msgl for word in chao):
        await message.add_reaction('😆')
        await msc.send(rchao())
        return

    # lời kêu
    if any(word in msgl for word in keu):
        await msc.send(rkeu())
        return

    # Khó
    if any(word in msgl for word in ['khó']):
        await message.add_reaction('👌')
        await msc.send(rkho())
        return

    # chửi
    if any(word in msgl for word in chui):
        await message.add_reaction('😡')
        await msc.send(rchui())
        return

    # ây da
    if any(word in msgl for word in ['ây da']):
        await msc.send('á à')
        return

    # ?
    if msg.startswith('?'):
        await msc.send(random.choice(['?', '???', 'what', 'sao', '??? cc à']))
        return

    # oke
    if any(word in msgl for word in ['hay', 'tốt', 'good', 'ngon']):
        await msc.send(random.choice(['quá đã', 'ngon']))
        return

    # buồn
    if any(word in msgl for word in buon):
        await message.add_reaction('😢')
        await msc.send(rbuon())
        return


client.add_cog(Player(client))
client.run(os.environ['TOKEN'])
# https://discord.com/api/oauth2/authorize?client_id=911855562361278565&permissions=8&scope=bot
