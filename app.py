import logging
import discord
import requests

from userprofile import UserProfile
from music import *
from discord.ext import commands
from discord import Embed
from discord import ui
from unibot_api import *

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

    embed = Embed()
    embed.set_image(url='https://storage.sekai.best/sekai-assets/stamp/stamp0168_rip/stamp0168/stamp0168.png')
    await ctx.send('Wonderhoy!!!', embed=embed)


@bot.command()
async def userinfo(ctx, userid='120513064353689609'):
    print(f'{ctx.author} asked for user info of {userid}')

    userprofile = UserProfile()
    userprofile.getprofile(userid=userid)

    embed = Embed()
    embed.add_field(name='Name', value=userprofile.name)
    embed.add_field(name='Rank', value=userprofile.rank)
    embed.add_field(name='User ID', value=userprofile.userid)

    await ctx.send(f'User Information about {userid}', embed=embed)


@bot.command()
async def songinfo(ctx, songid):
    print(f'{ctx.author} asked for song info for {songid}')

    music = Music(int(songid))

    if music.songid == 0:
        await ctx.send(f'找不到这首歌喵')
    else:
        embed = Embed()
        embed.title = music.title
        embed.description = music.pronunciation
        embed.add_field(name='编号', value=music.songid)
        embed.add_field(name='标签', value=music.get_tag_str())
        embed.add_field(name='类别', value=music.get_categories_str())
        embed.add_field(name='作词', value=music.lyricist)
        embed.add_field(name='编曲', value=music.composer)
        embed.add_field(name='作曲', value=music.arranger)
        embed.add_field(name='难度', value=music.get_diff_str(), inline=False)
        embed.add_field(name='物量', value=music.get_note_count_str(), inline=False)
        embed.set_thumbnail(url=f'https://storage.sekai.best/sekai-assets/music/jacket/{music.asset_bundle_name}_rip/{music.asset_bundle_name}.png')

        await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    view = ui.View()
    view.add_item(ui.Button(label='test'))

    embed = Embed()
    embed.add_field(name='Name', value='')

    await ctx.send("test", embed=embed, view=view)


bot.run('MTA2ODI3MzI5MTczNjkxMTk1Mg.GiHJi3.gTptYkmcx8A6H74uN7AIqjQbsydmtJ164e-5qY')
