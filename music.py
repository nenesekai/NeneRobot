import json

from config import masterdb


def get_music(songid):
    with open(f'{masterdb}/musics.json', mode='r', encoding='utf-8') as f:
        musics_db = json.load(f)

    for music in musics_db:
        if music['id'] == songid:
            return music

    return 0


def get_music_tag(songid):
    with open(f'{masterdb}/musicTags.json', mode='r', encoding='utf-8') as f:
        music_tags_db = json.load(f)

    tag = []

    for music_tag in music_tags_db:
        if music_tag['musicId'] == songid:
            tag.append(music_tag['musicTag'])

    return tag


def get_diff_and_note_count(songid):
    with open(f'{masterdb}/musicDifficulties.json', mode='r', encoding='utf-8') as f:
        music_diffs_db = json.load(f)

    diff = [0, 0, 0, 0, 0]
    note_count = [0, 0, 0, 0, 0]

    for music_diff in music_diffs_db:
        if music_diff['musicId'] == songid:
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

    def __init__(self, songid):
        music_raw = get_music(songid)

        self.songid = songid

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
            self.tags = get_music_tag(songid)

            self.diff, self.note_count = get_diff_and_note_count(songid)
        except():
            pass

    def get_tag_str(self):
        tag_str = ''

        for tag in self.tags:
            tag_str += tag + ', '

        return tag_str[:-2]

    def get_categories_str(self):
        categories_str = ''

        for category in self.categories:
            categories_str += category + ', '

        return categories_str[:-2]

    def get_diff_str(self):
        return f'Easy: {self.diff[0]}, Normal: {self.diff[1]}, Hard: {self.diff[2]}, Expert: {self.diff[3]}, Master: {self.diff[4]}'

    def get_note_count_str(self):
        return f'Easy: {self.note_count[0]}, Normal: {self.note_count[1]}, Hard: {self.note_count[2]}, Expert: {self.note_count[3]}, Master: {self.note_count[4]}'