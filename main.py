# LIBRARY
import discord
from discord.ext import commands
from config import settings
from discord import FFmpegPCMAudio, Activity, ActivityType
from discord.ext.commands import Bot
import os 
import json
import time
import random
import discordSuperUtils
import asyncio
import datetime 
from discord.ext import commands, tasks 
from discord.utils import get 
import sys 
import youtube_dl
from youtube_dl import YoutubeDL
from asyncio import sleep
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord_together import DiscordTogether
import discord
import aiohttp
import DiscordUtils
import typing
from aiohttp import ClientSession
from typing import Union, Optional

# ()
intents = discord.Intents.all()
client = commands.Bot(command_prefix = settings['prefix'],intents=intents, help_command=None) 
badwords = ["шлюха", "мать", "еблан", "сучка", "безмамный", "негры"]
os.chdir(r'C:/golembot')
invtrck = DiscordUtils.InviteTracker(client)
class LOGINFO :
	CHANNELID = 1096439018167734363
	GUILDID = 1043209850475262023

# START AND STATUS
@client.event
async def on_ready():
  guilds = len(client.guilds)
  info = "!"
  print("[{}] bot ready!.".format(info)) 
  voice_channel = client.get_channel(1095577158107271279) #айди голосового канала
  player = await voice_channel.connect()
  player.play(FFmpegPCMAudio("http://s02.fjperezdj.com:8006/live")) #ссылка на радио. Указывать в кавычках.
  client.togetherControl = await DiscordTogether(settings['token'])
  while True:
    await client.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = f',help', type = discord.ActivityType.playing)) #Инфа о количестве серверов, на котором находится бот.
    await asyncio.sleep(15)
    members = 0
    for guild in client.guilds:
      for member in guild.members:
        members += 1
    await client.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = f'за {members} участниками', type = discord.ActivityType.watching)) #Общее количество участников, за которыми следит бот (Находятся на серверах)
    await asyncio.sleep(15)

# RELOAD BOT  
@client.command()
@has_permissions(administrator = True)
async def reload(ctx):
	embed = discord.Embed(title = f"GOLEM", description = "Reloading...", color = 0xff0000)
	embedmas = await ctx.send(embed=embed)
	await asyncio.sleep(2)
	emb = discord.Embed(title = f"GOLEM", description = "Reloaded", color = 0x00ff3a)
	embedmas = await ctx.send(embed=emb)
	await os.execv(sys.executable, ["python"] + sys.argv) 

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "{}, у вас нету прав!".format(ctx.message.author)
        await client.send_message(ctx.message.channel, text)

# COMMAND .help
@client.group(invoke_without_command = True)
async def help(ctx):
    emb = discord.Embed( title = 'Помощь по командам:', colour= 0xf7ff00)

    emb.add_field( name = '**Основные команды**', value = '', inline = True )

    emb.add_field( name = '`,roll`', value = '*Кинуть кости*', inline = False )
    emb.add_field( name = '`,avatar`', value = '*Вывод аватара пользователя*', inline = False )
    emb.add_field( name = '`,youtube`', value = '*Начать активность ютуб*', inline = False )
    emb.add_field( name = '`,about`', value = '*Информация о участнике*', inline = False )
    emb.add_field( name = '`,meme`', value = '*Случайный мем с Reddit*', inline = False )
    emb.add_field( name = '`,ball`', value = '*Спросить у шара*', inline = False )

    emb.add_field( name = '**Команды для модерации**', value = ',help <команда> (работает для команд модерации)', inline = True )

    emb.add_field( name = '`,ban`', value = '*Забанить участника*', inline = False )
    emb.add_field( name = '`,mute`', value = '*Замьютить участника*', inline = False )
    emb.add_field( name = '`,kick`', value = '*Кикнуть участника*', inline = False )
    emb.add_field( name = '`,unban`', value = '*Разбанить участника*', inline = False )
    emb.add_field( name = '`,unmute`', value = '*Размьютить участника*', inline = False )

    emb.add_field( name = 'Сайт бота:', value = 'https://heawik.ru/village', inline = False )

    await ctx.send( embed = emb )

# COMMAND .help ban
@help.command()
async def ban(ctx):
    emb = discord.Embed(colour=discord.Color.blue())

    emb.add_field( name = '**Чтобы забанить воспользуйтесь следующей командой:**', value = '`,ban @Нарушитель Время(дни) Причина`', inline = False )

    await ctx.send( embed=emb )

# COMMAND .help unban
@help.command()
async def unban(ctx):
    emb = discord.Embed(colour=discord.Color.blue())

    emb.add_field( name = '**Чтобы разбанить воспользуйтесь следующей командой:**', value = '`,unban @Участник#1234`', inline = False )
    emb.add_field( name = '*При случае если разбан не сработал, зайдите в настройки сервера -> Баны и просто таким образом разбаньте*', value = '*бот может отказываться*', inline = False )

    await ctx.send( embed=emb )

# COMMAND .help mute
@help.command()
async def mute(ctx):
    emb = discord.Embed(colour=discord.Color.blue())

    emb.add_field( name = '**Чтобы заглушить участника воспользуйтесь следующей командой:**', value = '`,mute @Нарушитель Время(минуты)`', inline = False )

    await ctx.send( embed=emb )

# COMMAND .help unmute
@help.command()
async def unmute(ctx):
    emb = discord.Embed(colour=discord.Color.blue())

    emb.add_field( name = '**Чтобы размутить воспользуйтесь следующей командой:**', value = '`,unmute @Участник`', inline = False )

    await ctx.send( embed=emb )

# COMMAND .help kick
@help.command()
async def kick(ctx):
    emb = discord.Embed(colour=discord.Color.blue())

    emb.add_field( name = '**Чтобы кикнуть воспользуйтесь следующей командой:**', value = '`,kick @Участник`', inline = False )

    await ctx.send( embed=emb )

# KICK
@client.command(pass_context=True)
@has_permissions(kick_members=True) 
async def kick(ctx, user: discord.Member):
    channel = client.get_channel(1080456995695509587)
    author = ctx.message.author
    emb = discord.Embed( title = 'Пинок из сервера', colour=discord.Color.red())
    emb.add_field( name = 'Кикнут:', value = f'{user}', inline = False )
    emb.add_field( name = 'Модератор:', value = f'{author.mention}', inline = False )
    await ctx.send( embed = emb )
    await channel.send(embed = emb)
    await ctx.guild.kick(user)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "{}, у вас недостаточно прав для этой команды или команда неправильно написана!".format(ctx.message.author)
        await client.send_message(ctx.message.channel, text)

# MUTE
@client.command(pass_context=True)
@has_permissions(mute_members=True) 
async def mute(ctx, member: discord.Member, time: int, reason):
    channel = client.get_channel(1080456995695509587)
    muterole = discord.utils.get(ctx.guild.roles, id = 1043222126670393414)
    emb = discord.Embed(title = 'Мьют', color=344462)
    emb.add_field(name="Заглушён:", value='{}'.format(member.mention))
    emb.add_field(name="Модератор", value = ctx.message.author.mention, inline = False)
    emb.add_field(name="Причина", value = reason, inline = False)
    await channel.send(embed = emb)
    await member.add_roles(muterole)
    await asyncio.sleep(time * 60)
    await member.remove_roles(muterole)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "{}, у вас недостаточно прав для этой команды или команда неправильно написана!".format(ctx.message.author)
        await client.send_message(ctx.message.channel, text)

# UNMUTE
@client.command(pass_context=True)
@has_permissions(mute_members=True)
async def unmute(ctx, member: discord.Member):
    channel = client.get_channel(1080456995695509587)
    muterole = discord.utils.get(ctx.guild.roles, id = 1043222126670393414)
    emb = discord.Embed(title = 'Размьют', color=344462)
    emb.add_field(name="Был разглушен:", value='{}'.format(member.mention))
    emb.add_field(name="Модератор:", value = ctx.message.author.mention, inline = False)
    await channel.send(embed = emb)
    await member.remove_roles(muterole)

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "{}, у вас недостаточно прав для этой команды или команда неправильно написана!".format(ctx.message.author)
        await client.send_message(ctx.message.channel, text)

# BAN
@client.command(pass_context=True)
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, days, reason):
    channel = client.get_channel(1080456995695509587)
    author = ctx.message.author
    await ctx.channel.purge(limit=0)
    emb = discord.Embed(title = 'Бан', color=344462)
    emb.add_field(name='Забанен:', value='{}'.format(member.mention))
    emb.add_field(name='Модератор:', value=f'{author.mention}')
    emb.add_field(name='Время:', value=f'{days} дней')
    emb.add_field(name='Причина:', value=f'{reason}')
    await channel.send(embed = emb)
    await member.ban(reason=reason)

# ROLL
@client.command()
async def roll(ctx, *arg):
    await ctx.reply(f'Итог: {random.randint(0, 10)}')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "{}, у вас недостаточно прав для этой команды или команда неправильно написана!".format(ctx.message.author)
        await client.send_message(ctx.message.channel, text)

# UNBAN
@client.command(pass_context=True)
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    channel = client.get_channel(1080456995695509587)
    author = ctx.message.author
    banned_users = await ctx.guild.bans()
    await ctx.channel.purge(limit=0)

    for ban_entry in banned_users:
        user = ban_entry.user
        emb = discord.Embed(title = 'Разбан', color=344462)
        emb.add_field(name='Разбанен:', value='{}'.format(member))
        emb.add_field(name='Модератор:', value=f'{author.mention}')
        await channel.send(embed = emb)
        await ctx.guild.unban(user)
        return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "{}, у вас недостаточно прав для этой команды или команда неправильно написана!".format(ctx.message.author)
        await client.send_message(ctx.message.channel, text)

# PRIVATE CREATING
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        if after.channel.id == 1100436231915048991:
            category = after.channel.category
            
            channel2 = await member.guild.create_voice_channel(
                name     = f' { member.display_name }', 
                category = category
            )
            
            await channel2.set_permissions(member, connect = True)
            await member.move_to(channel2)

            def check(x, y, z): return len(channel2.members) == 0
            
            await client.wait_for('voice_state_update', check = check)
            await channel2.delete() 

# AVATAR
@client.command()
async def avatar(ctx, member: discord.Member  = None):
    if member == None:#если не упоминать участника тогда выводит аватар автора сообщения
        member = ctx.author
    embed = discord.Embed(color = 0x22ff00, title = f"Аватар - {member.name}", description = f"[СКачать аватар]({member.avatar})")
    embed.set_thumbnail(url=member.avatar)
    await ctx.send(embed = embed)

# ABOUT
@client.command(pass_context=True)
async def about(ctx,member:discord.Member = None, guild: discord.Guild = None):
    if member == None:
        emb = discord.Embed(title="Информация о участнике:", color=ctx.message.author.color)
        emb.add_field(name="Никнейм:", value=ctx.message.author.display_name,inline=False)
        emb.add_field(name="ID:", value=ctx.message.author.id,inline=False)
        t = ctx.message.author.status
        if t == discord.Status.online:
            d = " В сети"

        t = ctx.message.author.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = ctx.message.author.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = ctx.message.author.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"

        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=ctx.message.author.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        emb.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title="Информация о участнике:", color=member.color)
        emb.add_field(name="Никнейм:", value=member.display_name,inline=False)
        emb.add_field(name="ID:", value=member.id,inline=False)
        t = member.status
        if t == discord.Status.online:
            d = " В сети"

        t = member.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = member.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = member.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"
        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=member.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        await ctx.send(embed = emb)

# COMMAND ,ball
@client.command()
async def ball(ctx, *, vopros):
	otvet1 = discord.Embed(title='', description="Да", color=discord.Color.blue())
	otvet2 = discord.Embed(title='', description="Нет", color=discord.Color.blue())
	otvet3 = discord.Embed(title='', description="Возможно", color=discord.Color.blue())
	otvet4 = discord.Embed(title='', description="Конечно что.... нет", color=discord.Color.blue())
	otvet5 = discord.Embed(title='', description="Даже не думай об этом!", color=discord.Color.blue())
	otvet6 = discord.Embed(title='', description="Спроси ещё раз", color=discord.Color.blue())
	otvet7 = discord.Embed(title='', description="Я не могу ответить на этот вопрос", color=discord.Color.blue())
	otvet8 = discord.Embed(title='', description="Не знаю", color=discord.Color.blue())
	embed=random.choice([otvet1, otvet2, otvet3, otvet4, otvet5, otvet6, otvet7, otvet8])
	await ctx.reply(embed=embed)

# COMMAND ,meme
@client.command()
async def meme(ctx):
	embed = discord.Embed(title = "", description = "")

	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r :
			res = await r.json()

			embed.set_image(url = res['data']['children'] [random.randint(0, 25)]['data']['url'])
			await ctx.reply(embed=embed)

# YOUTUBE TOGETHER
defaultApplications = {
     'youtube': '880218394199220334'
}

@client.command()
async def youtube(ctx):
     link = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
     await ctx.send(f"Чтобы зайти, перейди по ссылке: \n{link}")

# LATENCY TEST
@client.command()
async def latency(ctx):
    await ctx.send(f"Проверка...")
    await asyncio.sleep(3)
    await ctx.send(f"{client.latency * 1000} мс")

@client.event
async def on_member_update(before, after):
    print(before.member.top_role)#выведет самую высокую роль до изменения
    print(after.member.top_role)#выведет самую высокую роль после изменения

@client.event
async def on_member_update(before, after):
    print('Before: ', before)
    print('After', after)

@client.event
async def on_guild_channel_create(channel):
    print('Channel name: ', channel.name)#выведет имя канала
    print('Channel category: ', channel.category)#выведет категорию где он находится
    print('Channel id: ', channel.id)#выведет айди канала
    print('Channel created at', channel.created_at)#выведет час и дату когда он был создан

@client.event
async def on_guild_update(before, after):
    print('Before guild name: ', before.guild.name)
    print('After guild name: ', after.guild.name)

    print('Before guild banner_url: ', before.guild.banner_url)#банер сервера до
    print('After guild banner_url: ', after.guild.banner_url)#банер сервера после

    print('Before guild icon_url: ', before.guild.icon_url)#значок сервера до
    print('After guild icon_url: ', after.guild.icon_url)#значок сервера после

# BOT STARTING
client.run(settings['token']) 