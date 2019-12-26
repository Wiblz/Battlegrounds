import numpy as np
from tawern_data import State, tawern_upgrade_cost, options_count, MINION_COST, REFRESH_COST, MAX_TIER
from player import Player
from pool import Pool


class RecruitmentStage:
    def __init__(self, generator):
        self.generator = generator
        self.pool = Pool(generator)

    def start_stage(self, players):
        '''
        Generates new minions in tawern for each player in 'players', unless the board is frozen.
        Increases starting gold by 1 (up to 10) and refreshes players gold.
        Decreases tawern upgrade cost by 1.

        Should be called at the start of each recruitment stage.

        TODO: Kick dead players (?)
        '''
        for player in players:
            player.state = State.RECRUITMENT
            player.refresh_gold()
            player.tawern_upgrade_cost -= 1

            if player.tawern_options is None:
                player.tawern_options = self.pool.generate_minions(player.tier)
            
            elif len(player.tawern_options) < options_count[player.tier]:
                player.tawern_options += self.pool.generate_minions(
                    tier=player.tier,
                    size=options_count[player.tier] - len(player.tawern_options)
                )

    def take_action(self, player: Player):
        action_space = self.generate_action_space(player)
        action = player.take_action(action_space)

        if action in ['ready, freeze']:
            player.state = State.READY
        
        if action == 'ready':
            player.tawern_options = None

        elif action == 'refresh':
            self.refresh_tawern(player)
        
        elif action == 'upgrade tawern':
            player.tier += 1
            player.tawern_upgrade_cost = tawern_upgrade_cost[player.tier]
    
        print(action)

    def refresh_tawern(self, player):
        self.pool.return_minions(player.tawern_options)
        player.tawern_options = self.pool.generate_minions(player.tier)

    def generate_action_space(self, player):
        action_space = []

        if player.state is State.RECRUITMENT:
            if player.gold >= MINION_COST and not player.hand.is_full():
                action_space.append('buy')

            if player.gold >= REFRESH_COST:
                action_space.append('refresh')

            if not player.hand.is_empty():
                action_space.append('play card')
            
            if player.tier != MAX_TIER and player.gold >= player.tawern_upgrade_cost:
                action_space.append('upgrade tawern')
            
            # reordering makes sense when 2 or more minions are present on the board
            if len(player.board.minions) > 1:
                action_space.append('reorder')

            if len(player.board.minions) > 0:
                action_space.append('sell')

            action_space += ['ready', 'freeze']
        elif player.state is State.DISCOVER:
            pass

        return action_space
