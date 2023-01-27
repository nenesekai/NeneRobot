import requests
import json

from config import api, masterdb, asset


class UserProfile(object):

    def __init__(self, user_id):
        self.user_id = user_id

        response = requests.get(f'{api}/user/{user_id}/profile', timeout=10)
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

        with open(f'{masterdb}/cards.json', 'r', encoding='utf-8') as f:
            cards = json.load(f)

        for card in cards:
            if card['id'] == leader_card['cardId']:
                if leader_card['defaultImage'] == 'special_training':
                    return f"{asset}/character/member_cutout/{card['assetbundleName']}/after_training/thumbnail_xl.png"
                else:
                    return f"{asset}/character/member_cutout/{card['assetbundleName']}/normal/thumbnail_xl.png"
