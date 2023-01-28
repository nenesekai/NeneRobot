import logging
from io import BytesIO

import discord
import config

from modules.userprofile import *
from modules.music import *
from modules.views import *
from discord.ext import commands
from discord import Embed
from discord import ui

# discord.py setup

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('<'), intents=intents)

# logging setup

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.command()
async def wonderhoy(ctx):
    print(f'{ctx.author} asked for wonderhoy (ID: {ctx.author.id})')
    await ctx.send(f'{config.ASSET}/stamp/stamp0168/stamp0168/stamp0168.png')


@bot.command()
async def bind(ctx, user_id):
    print(f'{ctx.author} wants to bind {user_id}')

    userprofile = UserProfile(user_id)

    if userprofile.user_id == 0:
        await ctx.reply(f'这个id获取不到任何数据喵')
        return

    if bind_user_id_with_discord_id(user_id, ctx.author.id):
        userprofile = UserProfile(user_id)

        await ctx.reply(f'成功绑定 {user_id}', embed=userprofile.get_discord_embed())
    else:
        view = ForceRebindView()
        await ctx.reply(f'绑定失败，当前账号已绑定{get_user_id_from_discord_id(ctx.author.id)}', view=view)
        await view.wait()
        if view.value:
            bind_user_id_with_discord_id(user_id, ctx.author.id, forced=True)
            await ctx.reply(f'成功绑定 {user_id}', embed=userprofile.get_discord_embed())


@bot.command()
async def userinfo(ctx, user_id=None):

    if user_id is None:
        user_id = get_user_id_from_discord_id(ctx.author.id)

        print(f'{ctx.author} (id: {ctx.author.id} ask for his profile: {user_id}')

        if user_id == 0:
            await ctx.reply(f'没有查询到，可能是你还没有绑定，请使用bind指令绑定你的pjsk账号')
        else:
            userprofile = UserProfile(user_id)
            await ctx.reply(embed=userprofile.get_discord_embed())

    else:
        print(f'{ctx.author} asked for user info of {user_id}')

        userprofile = UserProfile(user_id)

        if userprofile.user_id == 0:
            await ctx.reply(f'找不到该用户喵')
        else:
            await ctx.reply(embed=userprofile.get_discord_embed())


@bot.command()
async def songinfo(ctx, *, alias):
    print(f'{ctx.author} asked for song info for {alias}')

    music_id = get_id_from_alias(alias)

    music = Music(int(music_id))

    if music.music_id == 0:
        await ctx.reply(f'找不到这首歌喵')
    else:
        await ctx.reply(embed=music.get_discord_embed())


@bot.command()
async def songinfoid(ctx, music_id):
    print(f'{ctx.author} asked for song info for {music_id}')

    music = Music(int(music_id))

    if music.music_id == 0:
        await ctx.reply(f'找不到这首歌喵')
    else:
        await ctx.reply(embed=music.get_discord_embed())


@bot.command()
async def userprofile(ctx, user_id=None):
    if user_id is None:
        print(f'{ctx.author} asked for his user profile')

        user_id = get_user_id_from_discord_id(ctx.author.id)

        if user_id == 0:
            await ctx.reply(f'没有查询到，可能是你还没有绑定，请使用bind指令绑定你的pjsk账号')
        else:
            up = UserProfile(user_id)
            img = up.generate_profile()

            with BytesIO() as image_binary:
                up.generate_profile().save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename=user_id + '_userprofile.png'))
    else:
        print(f'{ctx.author} asked for user profile of {user_id}')

        up = UserProfile(user_id)

        if up.user_id == 0:
            await ctx.reply(f'找不到该用户喵')
        else:
            img = up.generate_profile()

            with BytesIO() as image_binary:
                up.generate_profile().save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename=user_id + '_userprofile.png'))


bot.run(config.TOKEN)
