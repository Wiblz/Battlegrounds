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

        for tier in tier_contents:
            self.pool[tier] = dict()
            cnt = count_per_minion[tier]

            for minion in tier_contents[tier]:
                self.pool[tier][minion] = cnt

    def start_stage(self, players):
        for player in players:
            if player.tawern_options is None:
                player.tawern_options = self.generate_options(player.tier)
            
            elif len(player.tawern_options) < options_count[player.tier]:
                player.tawern_options += self.generate_options(
                    tier=player.tier,
                    size=options_count[player.tier] - len(player.tawern_options)
                )

    def next_action(self, player: Player):
        action = self.recruitment_action(player)
        if action in ['ready, freeze']:
            player.ready = True
        
        if action == 'ready':
            player.tawern_options = None

        elif action == 'refresh':
            player.refresh()
        
        elif action == 'upgrade tawern':
            player.tier += 1
            player.tawern_upgrade_cost = tawern_upgrade_cost[player.tier]
    
        print(action)
    
    def on_buy(self, name):
        pass

    def on_sell(self, minion):
        pass

    def refresh(self, player):
        self.return_to_pool(player.tawern_options)
        player.tawern_options = self.generate_options(player.tier)

    def return_to_pool(self, options):
        for option in options:
            self.pool[minions[option]['tier']][option] += 1

    def generate_options(self, tier, size=None):
        size = size or options_count[tier]
        active_pool = []
        probabilities = np.array([])

        for t in range(1, tier + 1):
            active_pool += list(self.pool[t].keys())
            probabilities = np.concatenate((probabilities, np.array(list(self.pool[t].values()))))

        probabilities /= probabilities.sum()
        options = self.generator.choice(np.array(active_pool), size=size, p=probabilities)
        
        for option in options:
            self.pool[minions[option]['tier']][option] -= 1

        return options

    def recruitment_action(self, player):
        options = []

        if player.gold >= MINION_COST:
            for i in range(len(player.tawern_options)):
                options.append(f'buy {i}')

        if player.gold >= REFRESH_COST:
            options.append('refresh')

        if len(player.board.minions) < MAX_BOARD_SIZE:
            options.append('play card')
        
        if player.tier != MAX_TIER and player.gold >= player.tawern_upgrade_cost:
            options.append('upgrade tawern')

        options += ['ready', 'freeze']
        
        if player.bot:
            action = random.choice(options)
        else:
            self.print_state(player)
            action = self.read_input(options) 
        
        return action
    
    def print_state(self, player):
        print('TAWERN\n')
        for i in range(len(player.tawern_options)):
            print(f'{i}. {player.tawern_options[i]}')

        print('\nHAND\n')
        for i in range(player.hand.size()):
            print(f'{i}. {player.hand.minions[i]}')

    def read_input(self, options):
        st = ''

        for i in range(len(options)):
            st += f'{i}. {options[i]}\n'
        
        return options[int(input(st))]
