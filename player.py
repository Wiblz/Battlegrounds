from tawern_data import tawern_upgrade_cost, State, MAX_GOLD
from hand import Hand
from board import Board
import random


class Player:
    def __init__(self):
        self.bot = True
        self.state = State.HERO_CHOICE

        self.tawern_options = None
        self.hand = Hand()
        self.board = Board()

        self.tier = 1
        self.tawern_upgrade_cost = tawern_upgrade_cost[self.tier + 1]
        self.turn_start_gold = 3
        self.gold = self.turn_start_gold
        self.hero = None
        self.last_opponent = None

    def is_ready(self):
        return self.state is State.HERO_CHOICE

    def choose_hero(self, options):
        self.hero = random.choice(options)
        self.state = State.READY

    def refresh_gold(self):
        if self.turn_start_gold != MAX_GOLD:
            self.turn_start_gold += 1
        
        self.gold = self.turn_start_gold

    def take_action(self, action_space):
        if self.bot:
            action = random.choice(action_space)
        else:
            self.print_state()
            action = self.read_input(action_space)

        return action

    def print_state(self):
        print('TAWERN\n')
        for i in range(len(self.tawern_options)):
            print(f'{i}. {self.tawern_options[i]}')

        print('\nHAND\n')
        for i in range(self.hand.size()):
            print(f'{i}. {self.hand.minions[i]}')

    def read_input(self, action_space):
        st = ''

        for i in range(len(action_space)):
            st += f'{i}. {action_space[i]}\n'
        
        return action_space[int(input(st))]
