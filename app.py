import logging
import discord
import config

from modules.userprofile import UserProfile
from modules.music import *
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
    await ctx.send(f'{config.asset}/stamp/stamp0168/stamp0168/stamp0168.png')


@bot.command()
async def userinfo(ctx, user_id='120513064353689609'):
    print(f'{ctx.author} asked for user info of {user_id}')

    userprofile = UserProfile(user_id)

    if userprofile.user_id == 0:
        await ctx.reply(f'找不到该用户喵')
    else:
        embed = Embed()
        embed.title = userprofile.name
        embed.description = userprofile.word
        embed.add_field(name='等级', value=userprofile.rank)
        embed.set_thumbnail(url=userprofile.get_profile_picture())

        await ctx.reply(embed=embed)

@bot.command()
async def songinfo(ctx, *, alias):
    print(f'{ctx.author} asked for song info for {alias}')

    music_id = get_id_from_alias(alias)

    music = Music(int(music_id))

    if music.music_id == 0:
        await ctx.reply(f'找不到这首歌喵')
    else:
        embed = Embed()
        embed.title = music.title
        embed.description = music.pronunciation
        embed.set_footer(text=f'作词：{music.lyricist}\t作曲：{music.composer}\t编曲：{music.arranger}')
        embed.add_field(name='编号', value=music.music_id)
        embed.add_field(name='标签', value=music.get_tags_str())
        embed.add_field(name='类别', value=music.get_categories_str())
        embed.add_field(name='难度', value=music.get_diffs_str(), inline=False)
        embed.add_field(name='物量', value=music.get_note_counts_str(), inline=False)
        embed.set_thumbnail(
            url=f'{config.asset}/music/jacket/{music.asset_bundle_name}/{music.asset_bundle_name}.png')

        await ctx.reply(embed=embed)


@bot.command()
async def songinfoid(ctx, music_id):
    print(f'{ctx.author} asked for song info for {music_id}')

    music = Music(int(music_id))

    if music.music_id == 0:
        await ctx.reply(f'找不到这首歌喵')
    else:
        embed = Embed()
        embed.title = music.title
        embed.description = music.pronunciation
        embed.set_footer(text=f'作词：{music.lyricist}\t作曲：{music.composer}\t编曲：{music.arranger}')
        embed.add_field(name='编号', value=music.music_id)
        embed.add_field(name='标签', value=music.get_tags_str())
        embed.add_field(name='类别', value=music.get_categories_str())
        embed.add_field(name='难度', value=music.get_diffs_str(), inline=False)
        embed.add_field(name='物量', value=music.get_note_counts_str(), inline=False)
        embed.set_thumbnail(url=f'{config.asset}/music/jacket/{music.asset_bundle_name}/{music.asset_bundle_name}.png')

        await ctx.reply(embed=embed)


bot.run(config.token)
