from types import MethodType
from minion import Minion
import random


class Minions:
    @staticmethod
    def new(player, card=None, name=None):
        board = player.board
        if card is not None:
            name = card.name

        # Tier 1
        if name == 'Alleycat':
            instance = Minion(name, 1, 1, 1, type='Beast')

            def battlecry(self):
                summoned = []
                if len(board.minions) < 7:
                    token = Minion('Cat', 1, 1, 1, type='Beast', summoned=True)
                    board.put(token, instance.get_position() + 1)
                    summoned.append(token)
                
                return summoned

            instance.battlecry = MethodType(battlecry, instance)
        elif name == 'Mecharoo':
            instance = Minion(name, 1, 1, 1, type='Mech')

            def deathrattle(self, position):
                summoned = []

                if len(board.minions) < 7:
                    token = Minion('Microbot', 1, 1, 1, type='Mech', summoned=True)
                    board.put(token, position)
                    summoned.append(token)
                
                return summoned

            instance.deathrattles.append(MethodType(deathrattle, instance))    
        elif name == 'Murloc Tidehunter':
            instance = Minion(name, 2, 1, 1, type='Murloc')

            def battlecry(self):
                summoned = []
                if not board.full():
                    token = Minion('Murloc', 1, 1, 1, type='Murloc', summoned=True)
                    board.put(token, instance.get_position() + 1)
                    summoned.append(token)
                
                return summoned

            instance.battlecry = MethodType(battlecry, instance)
        elif name == 'Selfless Hero':
            instance = Minion(name, 2, 1, 1)

            def deathrattle(self, position):
                if len(board.minions) > 0:
                    minion = random.choice(board.minions)
                    minion.bubble = True

                return []                                       # no new minions summoned

            instance.deathrattles.append(MethodType(deathrattle, instance))
        elif name == 'Rockpool Hunter':
            instance = Minion(name, 2, 3, 1, type='Murloc')

            def battlecry(self, target):
                target.attack += 1
                target.health += 1

                return []

            instance.valid_targets = board.murlocs
            instance.targeted_battlecry = MethodType(battlecry, instance)
        elif name == 'Vulgar Homunculus':
            instance = Minion(name, 2, 4, 1, type='Demon', taunt=True)

            def battlecry(self):
                player.hero.hp -= 2

                return []

            instance.battlecry = MethodType(battlecry, instance)
        elif name == 'Wrath Weaver':
            instance = Minion(name, 1, 1, 1)

            def trigger(self):
                player.hero.hp -= 1
                self.attack += 2
                self.health += 2

            def on_play(self):
                board.on_demon_played.append(self)
            
            instance.on_play = MethodType(on_play, instance)
            instance.trigger = MethodType(trigger, instance)
        elif name == 'Micro Machine':
            instance = Minion(name, 1, 2, 1, type='Mech')
            
            def trigger(self):
                self.attack += 1

            def on_play(self):
                board.on_turn_start.append(self)

            instance.on_play = MethodType(on_play, instance)
            instance.trigger = MethodType(trigger, instance)
        elif name == 'Murloc Tidecaller':
            instance = Minion(name, 1, 2, 1, type='Murloc')

            def trigger(self):
                print('Triggered!')
                self.attack += 1

            def on_play(self):
                board.on_murloc_summoned.append(self)

            instance.on_play = MethodType(on_play, instance)
            instance.trigger = MethodType(trigger, instance)
        elif name == 'Dire Wolf Alpha':
            instance = Minion(name, 2, 2, 1, type='Beast')

            def add_effect(self, target):
                target.effects.append(self)

                target.attack += 1
            
            def remove_effect(self, target):
                target.effects.remove(self)

                target -= 1
            
            instance.add_effect = MethodType(add_effect, instance)
            instance.remove_effect = MethodType(remove_effect, instance)
        elif name == 'Righteous Protector':
            instance = Minion(name, 1, 1, 1, taunt=True, bubble=True)
        elif name == 'Voidwalker':
            instance = Minion(name, 1, 3, 1, type='Demon', taunt=True)

        # Tier 2
        elif name == 'Spawn of N\'Zoth':
            instance = Minion(name, 2, 2, 2)

            def deathrattle(self, position):
                for minion in board.minions:
                    minion.attack += 1
                    minion.health += 1

                return []

            instance.deathrattles.append(MethodType(deathrattle, instance))
        elif name == 'Kindly Grandmother':
            instance = Minion(name, 1, 1, 2, type='Beast')

            def deathrattle(self, position):
                summoned = []
                if not board.full():
                    token = Minion('Big Bad Wolf', 3, 2, 1, type='Beast')
                    board.put(token, position)
                    summoned.append(token)

                return summoned
            
            instance.deathrattles.append(MethodType(deathrattle, instance))
        elif name == 'Mounted Raptor':
            instance = Minion(name, 3, 2, 2, type='Beast')

            def deathrattle(self, position):
                summoned = []
                if not board.full():
                    minion_name = random.choice([
                        'Righteous Protector',
                        'Selfless Hero',
                        # 'Wrath Weaver'            # TODO: test if this is possible
                        'Alleycat',
                        'Voidwalker',
                        'Mecharoo',
                        'Murloc Tidecaller',
                        # 'Nathrezim Overseer',     # and this
                        'Pogo-Hopper',
                        'Shifter Zerus',
                        'Toxfin'
                    ])
                    minion = Minions.new(player=player, name=minion_name)
                    board.put(minion, position)
                    summoned.append(minion)

                return summoned
            
            instance.deathrattles.append(MethodType(deathrattle, instance))
        elif name == 'Rat Pack':
            instance = Minion(name, 2, 2, 2, type='Beast')

            def deathrattle(self, position):
                summoned = []
                for _ in range(self.attack):
                    if not board.full():
                        token = Minion(name, 1, 1, 1, type='Beast', summoned=True)
                        board.put(token, position)
                        summoned.append(token)

                return summoned

            instance.deathrattles.append(MethodType(deathrattle, instance))
        elif name == 'Scavenging Hyena':
            instance = Minion(name, 2, 2, 2, type='Beast')

            def trigger(self):
                self.attack += 2
                self.health += 1

            def on_play(self):
                board.on_beast_died.append(self)

            instance.on_play = MethodType(on_play, instance)
            instance.trigger = MethodType(trigger, instance)
        elif name == 'Nathrezim Overseer':
            instance = Minion(name, 2, 4, 2, type='Demon')

            def battlecry(self, target):
                target.attack += 2
                target.health += 2

                return []
            
            instance.targeted_battlecry = MethodType(battlecry, instance)
            instance.valid_targets = board.demons
        elif name == 'Annoy-o-Tron':
            instance = Minion(name, 1, 2, 2, type='Mech', taunt=True, bubble=True)
        elif name == 'Harvest Golem':
            instance = Minion(name, 2, 3, 2, type='Mech')

            def deathrattle(self, position):
                summoned = []
                if not board.full():
                    token = Minion(name, 2, 1, 1, type='Mech', summoned=True)
                    board.put(token, position)
                    summoned.append(token)

                return summoned
            
            instance.deathrattles.append(MethodType(deathrattle, instance))
        elif name == 'Kaboom Bot':
            instance = Minion(name, 2, 2, 2, type='Mech')

            def deathrattle(self, position):
                target = player.current_opponent.board.get_random()
                board.damage(target, 4)

                return []
            
            instance.deathrattles.append(MethodType(deathrattle, instance))
        elif name == 'Metaltooth Leaper':
            instance = Minion(name, 3, 3, 2, type='Mech')

            def battlecry(self):
                for mech in board.mechs:
                    mech.attack += 2
                    
                return []
            
            instance.battlecry = MethodType(battlecry, instance)
        elif name == 'Pogo-Hopper':
            instance = Minion(name, 1, 1, 2, type='Mech')

            def battlecry(self):
                self.attack += board.pogos_played * 2
                self.health += board.pogos_played * 2
                    
                return []
            
            def on_play(self):
                board.pogos_played += 1

            instance.battlecry = MethodType(battlecry, instance)
            instance.on_play = MethodType(on_play, instance)
        elif name == 'Nightmare Amalgam':
            instance = Minion(name, 3, 4, 2, type='All')
        elif name == 'Shielded Minibot':
            instance = Minion(name, 2, 2, 2, type='Mech', bubble=True)
        elif name == 'Murloc Warleader':
            instance = Minion(name, 3, 3, 2, type='Murloc')

            def add_effect(self, target):
                target.attack += 2

            def remove_effect(self, target):
                target.attack -= 2

            def on_play(self):
                pass

        elif name == 'Psych-o-Tron':
            instance = Minion(name, 3, 4, 3, type='Mech', taunt=True, bubble=True)
        
        instance.board = board
        if card is not None:
            instance.attack += card.attack_buff
            instance.health += card.health_buff

        return instance


class Heroes:
    @staticmethod
    def new(name, board):
        raise NotImplementedError
