import json
import requests

from config import API, MASTER_DB, ASSET, MONGODB
from discord import Embed


def get_id_from_alias(alias):
    response = requests.get(f'{API}/getsongid/{alias}')
    data = response.json()

    if data['status'] == 'success':
        return data['musicId']
    else:
        return 0


def get_music(music_id):
    musics = requests.get(url=f'{MASTER_DB}/musics.json').json()

    for music in musics:
        if music['id'] == music_id:
            return music

    return 0


def get_music_tag(music_id):
    music_tags = requests.get(url=f'{MASTER_DB}/musicTags.json').json()

    tag = []

    for music_tag in music_tags:
        if music_tag['musicId'] == music_id:
            tag.append(music_tag['musicTag'])

    return tag


def get_diff_and_note_count(music_id):
    music_diffs_db = requests.get(url=f'{MASTER_DB}/musicDifficulties.json').json()

    diff = [0, 0, 0, 0, 0]
    note_count = [0, 0, 0, 0, 0]

    for music_diff in music_diffs_db:
        if music_diff['musicId'] == music_id:
            if music_diff['musicDifficulty'] == 'easy':
                diff[0] = music_diff['playLevel']
                note_count[0] = music_diff['totalNoteCount']
            if music_diff['musicDifficulty'] == 'normal':
                diff[1] = music_diff['playLevel']
                note_count[1] = music_diff['totalNoteCount']
            if music_diff['musicDifficulty'] == 'hard':
                diff[2] = music_diff['playLevel']
                note_count[2] = music_diff['totalNoteCount']
            if music_diff['musicDifficulty'] == 'expert':
                diff[3] = music_diff['playLevel']
                note_count[3] = music_diff['totalNoteCount']
            if music_diff['musicDifficulty'] == 'master':
                diff[4] = music_diff['playLevel']
                note_count[4] = music_diff['totalNoteCount']

    return diff, note_count


class Music(object):

    def __init__(self, music_id):
        music_raw = get_music(music_id)

        self.music_id = music_id

        try:
            self.title = music_raw['title']
            self.pronunciation = music_raw['pronunciation']
            self.lyricist = music_raw['lyricist']
            self.composer = music_raw['composer']
            self.arranger = music_raw['arranger']
            self.dancer_count = music_raw['dancerCount']
            self.asset_bundle_name = music_raw['assetbundleName']
            self.published_at = music_raw['publishedAt']
            self.categories = music_raw['categories']
            self.tags = get_music_tag(music_id)

            self.diff, self.note_count = get_diff_and_note_count(music_id)
        except:
            self.music_id = 0

    def get_tags_str(self):
        tag_str = ''

        for tag in self.tags:
            tag_str += tag + ', '

        return tag_str[:-2]

    def get_categories_str(self):
        categories_str = ''

        for category in self.categories:
            categories_str += category + ', '

        return categories_str[:-2]

    def get_diffs_str(self):
        return f'Easy: {self.diff[0]}, Normal: {self.diff[1]}, Hard: {self.diff[2]}, Expert: {self.diff[3]}, Master: {self.diff[4]}'

    def get_note_counts_str(self):
        return f'Easy: {self.note_count[0]}, Normal: {self.note_count[1]}, Hard: {self.note_count[2]}, Expert: {self.note_count[3]}, Master: {self.note_count[4]}'

    def get_cover_url(self):
        return f'{ASSET}/music/jacket/{self.asset_bundle_name}/{self.asset_bundle_name}.png'

    def get_discord_embed(self):
        embed = Embed()
        embed.title = self.title
        embed.description = self.pronunciation
        embed.set_footer(text=f'作词：{self.lyricist}\t作曲：{self.composer}\t编曲：{self.arranger}')
        embed.add_field(name='编号', value=self.music_id)
        embed.add_field(name='标签', value=self.get_tags_str())
        embed.add_field(name='类别', value=self.get_categories_str())
        embed.add_field(name='难度', value=self.get_diffs_str(), inline=False)
        embed.add_field(name='物量', value=self.get_note_counts_str(), inline=False)
        embed.set_thumbnail(url=self.get_cover_url())

        return embed