from tawern_data import tawern_upgrade_cost
import random


class Player:
    def __init__(self):
        self.tier = 1
        self.tawern_upgrade_cost = tawern_upgrade_cost[self.tier + 1]
        self.max_gold = 3
        self.gold = self.max_gold
        self.hero = None
        self.last_opponent = None

    def choose_hero(self, options):
        self.hero = random.choice(options)
