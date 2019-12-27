from recruitment import RecruitmentStage
from battle import BattleStage
from player import Player
from tawern_data import heroes
import random
import numpy as np


class Game:
    def __init__(self):
        self.generator = np.random.default_rng()

        self.recruitment = RecruitmentStage(self.generator)
        self.battle = BattleStage(self.generator)
        self.players = [Player(i) for i in range(8)]
        self.players[0].bot = False                   # uncomment to try interactive mode

    def offer_heroes(self):
        for i in range(8):
            options = []
            for _ in range(2 if i < 4 else 3):
                opt = random.choice(heroes)
                heroes.remove(opt)
                options.append(opt)
            self.players[i].choose_hero(options)
            # print(options, self.players[i].hero)
            

    def start(self):
        # Main game loop
        self.offer_heroes()
        
        while True:
            input('next stage')
            self.recruitment.start_stage(self.players)
            ready = False
            while not ready:
                ready = True
                for player in self.players:
                    if not player.is_ready():
                        self.recruitment.take_action(player)
                        ready = False
            

if __name__ == '__main__':
    game = Game()
    game.start()
