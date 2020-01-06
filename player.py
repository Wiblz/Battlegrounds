from tawern_data import tawern_upgrade_cost, State, MAX_GOLD
from hand import Hand
from hero import Hero
from board import Board
import numpy as np
import random


class Player:
    def __init__(self, id):
        self.bot = True
        self.id = id
        self.state = State.HERO_CHOICE
        self.battlecry_triggered_minion = None
        self.minion_picked = None

        self.tawern_options = None
        self.hand = Hand()
        self.board = Board()

        self.tier = 1
        self.tawern_upgrade_cost = tawern_upgrade_cost[self.tier] + 1   # 'workaround'
        self.turn_start_gold = 2                                        # and this one
        self.gold = self.turn_start_gold
        self.hero = None
        self.last_opponent = None
        self.current_opponent = None
        
        self.debug_actions = []

    def is_ready(self):
        return self.state is State.READY

    def choose_hero(self, options):
        self.hero = Hero(random.choice(options))
        self.state = State.READY

    def refresh_gold(self):
        if self.turn_start_gold != MAX_GOLD:
            self.turn_start_gold += 1
        
        self.gold = self.turn_start_gold

    def choose_action(self, action_space):
        if self.bot:
            return np.random.randint(len(action_space))
            # action = random.choice(action_space)
        else:
            self.print_state()
            # action = self.read_input(action_space)
            return self.read_input(action_space=action_space)

    def choose_minion(self, minions):
        if self.bot:
            return random.choice(minions)
        else:
            return minions[self.read_input(minions=minions)]

    def choose_board_slot(self):
        if self.bot:
            return np.random.randint(len(self.board.minions) + 1)
        else:
            print(f'Where? (0 - {len(self.board.minions)})\n')
            return int(input())

    def print_state(self):
        print(f'TAWERN -- {self.gold} gold -- {self.hero.hp} hp -- {self.tawern_upgrade_cost} upgr')
        for i in range(len(self.tawern_options)):
            print(f'{i}. {self.tawern_options[i]}')

        print('\nHAND')
        for i in range(self.hand.size()):
            print(f'{i}. {self.hand.cards[i]}')
        
        print()

    def read_input(self, action_space=None, minions=None):
        st = ''

        if action_space is not None:
            for i in range(len(action_space)):
                st += f'{i}. {action_space[i]}\n'
        else:
            for i in range(len(minions)):
                st += f'{i}. {minions[i]}\n'
        
        # return action_space[int(input(st))]
        return int(input(st))
