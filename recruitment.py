import numpy as np
from tawern_data import State, tawern_upgrade_cost, options_count, MINION_COST, REFRESH_COST, MAX_TIER, MAX_GOLD
from player import Player
from pool import Pool
from card import MinionCard, Coin, RecruitmentMap
from factories import Minions


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
            player.debug_actions.append(f'Play {card} card')
            player.hand.cards.remove(card)

            if isinstance(card, MinionCard):
                player.state = State.PLAYING_MINION
                player.minion_picked = Minions.new(card=card, player=player)
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
            slot = player.choose_board_slot()

            if player.minion_picked.targeted_battlecry is not None and \
               len(player.minion_picked.valid_targets) > 0:
                player.board.put(player.minion_picked, slot)
                player.debug_actions.append(f'Play {player.minion_picked} to {slot} slot with targeted battlecry')
                player.state = State.CHOOSING_BATTLECRY_TARGET
            else:
                player.board.play(minion=player.minion_picked, slot=slot)
                player.state = State.RECRUITMENT
                player.debug_actions.append(f'Play {player.minion_picked} to {slot} slot')
                player.minion_picked = None

        elif player.state is State.CHOOSING_BATTLECRY_TARGET:
            player.state = State.RECRUITMENT
            target = player.choose_minion(player.minion_picked.valid_targets)
            player.debug_actions.append(f'Apply battlecry of {player.minion_picked} to {target}')
            player.board.handle_targeted_battlecry(player.minion_picked, target)
            player.minion_picked = None

        elif player.state is State.PLACING_MINION:
            player.state = State.RECRUITMENT
            slot = player.choose_board_slot()
            player.board.put(player.minion_picked, slot)
            player.debug_actions.append(f'Place {player.minion_picked} to {slot} slot')
            player.minion_picked = None

        elif player.state is State.CHOOSING_MINION_TO_BUY:
            player.state = State.RECRUITMENT
            minion = player.choose_minion(player.tawern_options)
            player.tawern_options.remove(minion)
            player.hand.cards.append(minion)
            player.gold -= 3
            player.debug_actions.append(f'Buy {minion}')

        elif player.state is State.CHOOSING_MINION_TO_SELL:
            player.state = State.RECRUITMENT
            minion = player.choose_minion(player.board.minions)
            player.board.minions.remove(minion)
            self.pool.return_minion(minion)
            if player.gold < MAX_GOLD:
                player.gold += 1
            player.debug_actions.append(f'Sell {minion}')

        elif player.state is State.CHOOSING_MINION_TO_MOVE:
            player.state = State.PLACING_MINION
            player.minion_picked = player.choose_minion(player.board.minions)
            player.board.remove(player.minion_picked)
            player.debug_actions.append(f'Move {minion}')

        print('Player', player.id, player.board.minions,
                                player.board.on_murloc_summoned)

    def refresh_tawern(self, player):
        self.pool.return_cards(player.tawern_options)
        player.tawern_options = self.pool.generate_minions(player.tier)

    def generate_recruitment_actions(self, player):
        action_space = []

        if player.gold >= MINION_COST and len(player.tawern_options) > 0 and not player.hand.is_full():
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
        if action in ['ready', 'freeze']:
            player.state = State.READY
            
        if action == 'ready':
            player.debug_actions.append('Ready')
            player.tawern_options = None

        elif action == 'refresh':
            player.gold -= 1
            player.debug_actions.append('Refresh tawern')
            self.refresh_tawern(player)
            
        elif action == 'upgrade tawern':
            player.debug_actions.append('Upgrade tawern')
            player.gold -= player.tawern_upgrade_cost
            player.tier += 1
            player.tawern_upgrade_cost = tawern_upgrade_cost[player.tier]
        
        elif action == 'sell':
            player.debug_actions.append('Sell')
            player.state = State.CHOOSING_MINION_TO_SELL

        elif action == 'buy':
            player.debug_actions.append('Buy')
            player.state = State.CHOOSING_MINION_TO_BUY

        elif action == 'reorder':
            player.debug_actions.append('Reorder')
            player.state = State.CHOOSING_MINION_TO_MOVE

        elif action == 'play card':
            player.debug_actions.append('Play card')
            player.state = State.CHOOSING_CARD

    def generate_card_choose_actions(self, player):
        action_space = []
    
        for card in player.hand.cards:
            if player.gold >= card.cost:
                action_space.append(f'play {card}')
        
        return action_space
