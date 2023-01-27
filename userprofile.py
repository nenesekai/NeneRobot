import requests
from config import *


class UserProfile(object):

    def __init__(self):
        self.name = ''
        self.rank = 0
        self.userid = ''
        self.twitter_id = ''
        self.word = ''
        self.all_perfect = [0, 0, 0, 0, 0]
        self.full_combo = [0, 0, 0, 0, 0]
        self.clear = [0, 0, 0, 0, 0]
        self.mvp = 0
        self.super_star = 0
        self.honors = {}
        self.high_score = 0

    def getprofile(self, userid):
        response = requests.get(f'{api}/user/{userid}/profile', timeout=10)
        data = response.json()

        self.userid = userid
        self.name = data['user']['userGamedata']['name']
        self.rank = data['user']['userGamedata']['rank']
        self.honors = data['userProfileHonors']

        try:
            self.twitter_id = data['userProfile']['twitterId']
        except():
            pass

        try:
            self.word = data['userProfile']['word']
        except():
            pass

