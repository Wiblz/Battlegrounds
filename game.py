from recruitment import RecruitmentStage
from battle import BattleStage
from player import Player
from tawern_data import heroes
import random


class Game:
    def __init__(self):
        self.recruitment = RecruitmentStage()
        self.battle = BattleStage()
        self.players = [Player() for i in range(8)]

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
            pass


if __name__ == '__main__':
    game = Game()
    game.start()
