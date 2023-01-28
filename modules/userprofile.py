import requests
import json

from config import API, MASTER_DB, ASSET
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from pymongo import MongoClient
from discord import Embed
from modules.utils import *


def get_user_id_from_discord_id(discord_id):
    client = MongoClient()
    database = client['project-sekai-helper']
    collection = database['binds']
    query_result = collection.find_one({'discordId': discord_id})

    if query_result is None:
        return 0
    else:
        return query_result['userId']


def bind_user_id_with_discord_id(user_id, discord_id, forced=False):
    client = MongoClient()
    database = client['project-sekai-helper']
    collection = database['binds']
    query_result = collection.find_one({'discordId': discord_id})

    if query_result is not None:
        if forced:
            collection.delete_many(query_result)
            collection.insert_one({'discordId': discord_id, 'userId': user_id})
            return True
        else:
            return False

    else:
        collection.insert_one({'discordId': discord_id, 'userId': user_id})
        return True


class UserProfile(object):

    def __init__(self, user_id):
        self.user_id = user_id

        response = requests.get(f'{API}/api/user/{user_id}/profile', timeout=10)
        data = response.json()

        self.raw_data = data

        response.close()

        if data.__len__() == 0:
            self.user_id = 0
            return

        self.name = data['user']['userGamedata']['name']
        self.rank = data['user']['userGamedata']['rank']

        try:
            self.twitter = data['userProfile']['twitterId']
        except:
            self.twitter = ''

        try:
            self.word = data['userProfile']['word']
        except:
            self.word = ''

        self.user_decks = [{}, {}, {}, {}, {}]
        self.user_profile_honors = [{}, {}, {}]

        for honor in data['userProfileHonors']:
            self.user_profile_honors[honor['seq'] - 1] = honor

        for i in range(0, 5):
            card_id = data['userDecks'][0]['member' + str(i + 1)]

            for card in data['userCards']:
                if card['cardId'] == card_id:
                    self.user_decks[i] = card

        try:
            self.character_id = data['userChallengeLiveSoloResults'][0]['characterId']
            self.high_score = data['userChallengeLiveSoloResults'][0]['highScore']
        except:
            pass

        self.characters = data['userCharacters']

        self.all_perfect = [0, 0, 0, 0, 0]
        self.full_combo = [0, 0, 0, 0, 0]
        self.clear = [0, 0, 0, 0, 0]

        self.mvp = 0
        self.superstar = 0

        musics = requests.get(url=f'{MASTER_DB}/musics.json').json()
        music_difficulties = requests.get(url=f'{MASTER_DB}/musicDifficulties.json').json()

        self.play_results = {}

        for music in musics:
            self.play_results[music['id']] = [0, 0, 0, 0, 0]

        for result in data['userMusicResults']:
            music_id = result['musicId']
            music_difficulty = result['musicDifficulty']
            play_result = result['playResult']

            self.mvp += result['mvpCount']
            self.superstar += result['superStarCount']

            if music_difficulty == 'easy':
                diff = 0
            elif music_difficulty == 'normal':
                diff = 1
            elif music_difficulty == 'hard':
                diff = 2
            elif music_difficulty == 'expert':
                diff = 3
            else:
                diff = 4

            try:
                if play_result == 'full_perfect' and self.play_results[music_id][diff] < 3:
                    self.play_results[music_id][diff] = 3
                elif play_result == 'full_combo' and self.play_results[music_id][diff] < 2:
                    self.play_results[music_id][diff] = 2
                elif play_result == 'clear' and self.play_results[music_id][diff] < 1:
                    self.play_results[music_id][diff] = 1
            except KeyError:
                pass

        for result in self.play_results.values():
            for diff in range(0, 5):
                if result[diff] == 3:
                    self.all_perfect[diff] += 1
                if result[diff] >= 2:
                    self.full_combo[diff] += 1
                if result[diff] >= 1:
                    self.clear[diff] += 1


    def get_profile_picture_url(self):
        cards = requests.get(url=f'{MASTER_DB}/cards.json').json()

        for card in cards:
            if card['id'] == self.user_decks[0]['cardId']:
                return get_card_thumbnail_url(card['assetbundleName'], self.user_decks[0]['defaultImage'] == 'special_training')

    def get_discord_embed(self):
        embed = Embed()
        embed.title = self.name
        embed.description = self.word
        embed.add_field(name='等级', value=self.rank)
        embed.set_thumbnail(url=self.get_profile_picture_url())

        return embed

    def generate_profile(self):
        img = Image.open('pictures/backgrounds/profile.png')
        cards = requests.get(url=f'{MASTER_DB}/cards.json').json()

        try:
            pfp = Image.open(requests.get(url=self.get_profile_picture_url(), stream=True).raw).resize((151, 151))
            _, _, _, mask = pfp.split()
            img.paste(pfp, (118, 51), mask)
        except:
            pass

        draw = ImageDraw.Draw(img)
        font_style = ImageFont.truetype("fonts/SourceHanSansCN-Bold.otf", 45)
        draw.text((295, 45), self.name, fill=(0, 0, 0), font=font_style)
        font_style = ImageFont.truetype("fonts/FOT-RodinNTLGPro-DB.ttf", 20)
        draw.text((298, 116), 'id:' + str(self.user_id), fill=(0, 0, 0), font=font_style)
        font_style = ImageFont.truetype("fonts/FOT-RodinNTLGPro-DB.ttf", 34)
        draw.text((415, 157), str(self.rank), fill=(255, 255, 255), font=font_style)
        font_style = ImageFont.truetype("fonts/FOT-RodinNTLGPro-DB.ttf", 22)
        draw.text((182, 318), str(self.twitter), fill=(0, 0, 0), font=font_style)

        font_style = ImageFont.truetype("fonts/FOT-RodinNTLGPro-DB.ttf", 29)
        draw.text((952, 141), f'{self.mvp}回', fill=(0, 0, 0), font=font_style)
        draw.text((1259, 141), f'{self.superstar}回', fill=(0, 0, 0), font=font_style)

        font_style = ImageFont.truetype("fonts/SourceHanSansCN-Medium.otf", 24)
        size = font_style.getsize(self.word)
        if size[0] > 480:
            draw.text((132, 388), self.word[:int(len(self.word) * (460 / size[0]))], fill=(0, 0, 0),
                      font=font_style)
            draw.text((132, 424), self.word[int(len(self.word) * (460 / size[0])):], fill=(0, 0, 0),
                      font=font_style)
        else:
            draw.text((132, 388), self.word, fill=(0, 0, 0), font=font_style)

        font_style = ImageFont.truetype("fonts/FOT-RodinNTLGPro-DB.ttf", 27)
        for diff in range(0, 5):
            text_width = font_style.getsize(str(self.clear[diff]))
            text_coordinate = (int(170 + 132 * diff - text_width[0] / 2), int(735 - text_width[1] / 2))
            draw.text(text_coordinate, str(self.clear[diff]), fill=(0, 0, 0), font=font_style)

            text_width = font_style.getsize(str(self.full_combo[diff]))
            text_coordinate = (int(170 + 132 * diff - text_width[0] / 2), int(735 + 133 - text_width[1] / 2))
            draw.text(text_coordinate, str(self.full_combo[diff]), fill=(0, 0, 0), font=font_style)

            text_width = font_style.getsize(str(self.all_perfect[diff]))
            text_coordinate = (int(170 + 132 * diff - text_width[0] / 2), int(735 + 2 * 133 - text_width[1] / 2))
            draw.text(text_coordinate, str(self.all_perfect[diff]), fill=(0, 0, 0), font=font_style)

        for i in range(0, 5):
            try:
                card_id = self.user_decks[i]['cardId']

                for card in cards:
                    if card['id'] == card_id:
                        asset_bundle_name = card['assetbundleName']

                pfp = Image.open(requests.get(url=get_card_thumbnail_url(asset_bundle_name, self.user_decks[i]['defaultImage'] == "special_training"), stream=True).raw)
                pfp = pfp.resize((128, 128))

                _, _, _, mask = pfp.split()
                img.paste(pfp, (111 + 128 * i, 488), mask)
            except:
                pass

        character_count = 0
        font_style = ImageFont.truetype("fonts/FOT-RodinNTLGPro-DB.ttf", 29)
        for i in range(0, 5):
            for j in range(0, 4):
                character_count += 1
                character_rank = 0
                for character in self.characters:
                    if character['characterId'] == character_count:
                        character_rank = character['characterRank']
                        break
                text_width = font_style.getsize(str(character_rank))
                text_coordinate = (int(920 + 183 * j - text_width[0] / 2), int(686 + 88 * i - text_width[1] / 2))
                draw.text(text_coordinate, str(character_rank), fill=(0, 0, 0), font=font_style)
        for i in range(0, 2):
            for j in range(0, 4):
                character_count += 1
                character_rank = 0
                for character in self.characters:
                    if character['characterId'] == character_count:
                        character_rank = character['characterRank']
                        break
                text_width = font_style.getsize(str(character_rank))
                text_coordinate = (int(920 + 183 * j - text_width[0] / 2), int(510 + 88 * i - text_width[1] / 2))
                draw.text(text_coordinate, str(character_rank), fill=(0, 0, 0), font=font_style)
                if character_count == 26:
                    break

        try:
            chara = Image.open(f'pictures/chara/chr_ts_{self.character_id}.png').resize((70, 70))
            _, _, _, mask = chara.split()
            img.paste(chara, (952, 293), mask)
            draw.text((1032, 315), str(self.high_score), fill=(0, 0, 0), font=font_style)
        except:
            pass

        if self.user_profile_honors[0].__len__() != 0:
            honor_pic = generate_honor(self.user_profile_honors[0], True).resize((266, 56))
            _, _, _, mask = honor_pic.split()
            img.paste(honor_pic, (104, 228), mask)

        if self.user_profile_honors[1].__len__() != 0:
            honor_pic = generate_honor(self.user_profile_honors[1], False).resize((126, 56))
            _, _, _, mask = honor_pic.split()
            img.paste(honor_pic, (375, 228), mask)

        if self.user_profile_honors[2].__len__() != 0:
            honor_pic = generate_honor(self.user_profile_honors[2], False).resize((126, 56))
            _, _, _, mask = honor_pic.split()
            img.paste(honor_pic, (508, 228), mask)

        return img
