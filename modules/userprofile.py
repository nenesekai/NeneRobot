import requests
import json

from config import API, MASTER_DB, ASSET
from pymongo import MongoClient
from discord import Embed


def get_user_id_from_discord_id(discord_id):
    client = MongoClient()
    database = client['project-sekai-helper']
    collection = database['binds']
    query_result = collection.find_one({'discordId': discord_id})

    if query_result is None:
        return 0
    else:
        return query_result['userId']


def bind_user_id_with_discord_id(user_id, discord_id):
    client = MongoClient()
    database = client['project-sekai-helper']
    collection = database['binds']
    query_result = collection.find_one({'discordId': discord_id})

    if query_result is not None:
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

        self.user_cards = data['userCards']
        self.user_decks = data['userDecks']
        self.user_profile_honors = data['userProfileHonors']

    def get_profile_picture(self):
        for user_card in self.user_cards:
            if user_card['cardId'] == self.user_decks[0]['leader']:
                leader_card = user_card

        cards = requests.get(url=f'{MASTER_DB}/cards.json').json()

        for card in cards:
            if card['id'] == leader_card['cardId']:
                if leader_card['defaultImage'] == 'special_training':
                    return f"{ASSET}/character/member_cutout/{card['assetbundleName']}/after_training/thumbnail_xl.png"
                else:
                    return f"{ASSET}/character/member_cutout/{card['assetbundleName']}/normal/thumbnail_xl.png"

    def get_discord_embed(self):
        embed = Embed()
        embed.title = self.name
        embed.description = self.word
        embed.add_field(name='等级', value=self.rank)
        embed.set_thumbnail(url=self.get_profile_picture())

        return embed
