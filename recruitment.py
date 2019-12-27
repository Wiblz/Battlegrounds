import numpy as np
from tawern_data import State, tawern_upgrade_cost, options_count, MINION_COST, REFRESH_COST, MAX_TIER, MAX_GOLD
from player import Player
from pool import Pool
from card import MinionCard, Coin, RecruitmentMap


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
        if player.state is State.RECRUITMENT:
            action_space = self.generate_recruitment_actions(player)
            action = action_space[player.choose_action(action_space)]
            self.handle_recruitment_action(player=player, action=action)
            
        elif player.state is State.CHOOSING_CARD:
            action_space = self.generate_card_choose_actions(player)
            card = player.hand.cards[player.choose_action(action_space)]

            if isinstance(card, MinionCard):
                player.state = State.PLAYING_MINION
                player.card_in_play = card
            elif isinstance(card, Coin):
                player.state = State.RECRUITMENT
                player.hand.cards.remove(card)
                if player.gold < MAX_GOLD:
                    player.gold += 1
            elif isinstance(card, RecruitmentMap):
                player.state = State.DISCOVER
                player.discover_options = [] # TODO: generate discover options
                player.gold -= 3
            # TODO: add banana
            # TODO: add triple reward

        elif player.state is State.PLAYING_MINION:
            pass

        elif player.state is State.PLACING_MINION:
            pass

        print(action)

    def refresh_tawern(self, player):
        self.pool.return_minions(player.tawern_options)
        player.tawern_options = self.pool.generate_minions(player.tier)

    def generate_recruitment_actions(self, player):
        action_space = []

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
        return action_space

    def handle_recruitment_action(self, player, action):
        if action in ['ready, freeze']:
            player.state = State.READY
            
        if action == 'ready':
            player.tawern_options = None

        elif action == 'refresh':
            player.gold -= 1
            self.refresh_tawern(player)
            
        elif action == 'upgrade tawern':
            player.gold -= player.tawern_upgrade_cost
            player.tier += 1
            player.tawern_upgrade_cost = tawern_upgrade_cost[player.tier]
        
        elif action == 'sell':
            player.state = State.CHOOSING_MINION_TO_SELL

        elif action == 'buy':
            player.state = State.CHOOSING_MINION_TO_BUY

        elif action == 'reorder':
            player.state = State.CHOOSING_MINION_TO_MOVE

        elif action == 'play card':
            player.state = State.CHOOSING_CARD

    def generate_card_choose_actions(self, player):
        action_space = []
    
        for card in player.hand.cards:
            if player.gold >= card.cost:
                action_space.append(f'play {card}')
        
        return action_space
