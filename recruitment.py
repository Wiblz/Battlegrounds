import numpy as np
import random
from tawern_data import *
from player import Player


class RecruitmentStage:
    def __init__(self, generator):
        self.generator = generator
        self.pool = dict()
        self.tier_sum = {
            1 : 216,
            2 : 240,
            3 : 221,
        }

        self.frozen = False
        self.current_options = dict()

        for tier in tier_contents:
            self.pool[tier] = dict()
            cnt = count_per_minion[tier]

            for minion in tier_contents[tier]:
                self.pool[tier][minion] = cnt

    def next_action(self, player: Player):
        if player not in self.current_options:
            self.current_options[player] = self.generate_options(player.tier)
        
        action = self.recruitment_action(player)
        print(action)
    
    def on_buy(self, name):
        pass

    def on_sell(self, minion):
        pass

    def refresh(self, previous_options, tier):
        self.return_to_pool(previous_options)
        return self.generate_options(tier)

    def return_to_pool(self, options):
        for option in options:
            self.pool[minions[option]['tier']][option] += 1

    def generate_options(self, tier):
        active_pool = []
        probabilities = np.array([])

        for t in range(1, tier + 1):
            active_pool += list(self.pool[t].keys())
            probabilities = np.concatenate((probabilities, np.array(list(self.pool[t].values()))))

        probabilities /= probabilities.sum()
        options = self.generator.choice(np.array(active_pool), size=options_count[tier], p=probabilities)
        
        for option in options:
            self.pool[minions[option]['tier']][option] -= 1

        return options

    def recruitment_action(self, player):
        options = []

        if player.gold > 2:
            for i in range(len(self.current_options[player])):
                options.append(f'buy {i}')

        if player.gold > 0:
            options.append('refresh')

        if len(player.board.minions) < 7:
            options.append('play card')
        
        if player.gold >= player.tawern_upgrade_cost:
            options.append('upgrade tawern')

        options += ['ready', 'freeze']
        
        if player.bot:
            choice = random.choice(options)
        else:
            self.print_tawern(self.current_options[player])
            choice = self.read_input(options) 
        
        if choice in ['ready', 'freeze']:
            player.ready = True
        
        return choice
    
    def print_tawern(self, tawern_minions):
        print('TAWERN\n')
        for i in range(len(tawern_minions)):
            print(f'{i}. {tawern_minions[i]}')

        print('\n')

    def read_input(self, options):
        st = ''

        for i in range(len(options)):
            st += f'{i}. {options[i]}\n'
        
        return options[int(input(st))]
