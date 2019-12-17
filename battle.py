import numpy as np


class BattleStage:
    def __init__(self, generator):
        self.generator = generator

    def determine_first_move(self,first_board, second_board):
        if len(first_board) > len(second_board):
            return 0
        elif len(first_board) < len(second_board):
            return 1
        return self.generator.randint(2)
    
    def start_battle(self, first_board, second_board):
        boards = [first_board, second_board]
        minions_alive = [len(first_board), len(second_board)]
        attack_order = [0, 0]

        turn = self.determine_first_move()

        first_board_taunts = filter(lambda minion: minion.taunt, first_board)
        second_board_taunts = filter(lambda minion: minion.taunt, second_board)

        # TODO: Finish
        while all([x > 0 for x in minions_alive]):
            boards[turn][attack_order[turn]].hit(self.generator.randint(minions_alive[turn]))