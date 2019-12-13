from minion import Minion
import random


class Minions:
    @staticmethod
    def new(name, board):
        if name == 'Alleycat':
            instance = Minion(name, 1, 1, 1, type='Beast')

            def battlecry(self):
                summoned = []
                if len(board.minions) < 7:
                    token = Minion('Cat', 1, 1, 1, type='Beast')
                    board.minions.insert(instance.get_position() + 1, token)
                    summoned.append(token)
                
                return summoned

            instance.battlecry = battlecry
        elif name == 'Mecharoo':
            instance = Minion(name, 1, 1, 1, type='Mech')

            def deathrattle(self, position):
                summoned = []

                if len(board.minions) < 7:
                    token = Minion('Microbot', 1, 1, 1, type='Mech')
                    board.minions.insert(position, token)
                    summoned.append(token)
                
                return summoned

            instance.deathrattles.append(deathrattle)    
        elif name == 'Murloc Tidehunter':
            instance = Minion(name, 2, 1, 1, type='Murloc')

            def battlecry(self):
                summoned = []
                if len(board.minions) < 7:
                    token = Minion('Murloc', 1, 1, 1, type='Murloc')
                    board.minions.insert(instance.get_position() + 1, token)
                    summoned.append(token)
                
                return summoned

            instance.battlecry = battlecry
        elif name == 'Selfless Hero':
            instance = Minion(name, 2, 1, 1)

            def deathrattle(self, position):
                if len(board.minions) > 0:
                    minion = random.choice(board.minions)
                    minion.bubble = True

                return []                                       # no new minions summoned

            instance.deathrattles.append(deathrattle)
        elif name == 'Rockpool Hunter':
            instance = Minion(name, 2, 3, 1, type='Murloc')

            def battlecry(self, target):
                target.attack += 1
                target.health += 1

                return []

            instance.battlecry = battlecry
        elif name == 'Vulgar Homunculus':
            instance = Minion(name, 2, 4, 1, type='Demon', taunt=True)

            def battlecry(self):
                self.hero.hp -= 2

                return []

            instance.battlecry = battlecry
        elif name == 'Wrath Weaver':
            instance = Minion(name, 1, 1, 1)

            def trigger(self, minion):
                self.hero.hp -= 1
                self.attack += 2
                self.health += 2

            def on_play(self):
                board.on_demon_played.append(self)
            
            instance.on_play = on_play
            instance.trigger = trigger
        elif name == 'Micro Machine':
            instance = Minion(name, 1, 2, 1, type='Mech')
            
            def trigger(self, minion):
                self.attack += 1

            def on_play(self):
                board.on_turn_start.append(self)

            instance.on_play = on_play
            instance.trigger = trigger
        elif name == 'Murloc Tidecaller':
            instance = Minion(name, 1, 2, 1, type='Murloc')

            def trigger(self, minion):
                self.attack += 1

            def on_play(self):
                board.on_murloc_summoned.append(self)

            instance.on_play = on_play
            instance.trigger = trigger
        elif name == 'Dire Wolf Alpha':
            instance = Minion(name, 2, 2, 1, type='Beast')

            def add_effect(self, target):
                target.effects.append(self)

                target.attack += 1
            
            def remove_effect(self, target):
                target.effects.remove(self)

                target -= 1
            
            instance.add_effect = add_effect
            instance.remove_effect = remove_effect
        elif name == 'Righteous Protector':
            instance = Minion(name, 1, 1, 1, taunt=True, bubble=True)
        elif name == 'Voidwalker':
            instance = Minion(name, 1, 3, 1, type='Demon', taunt=True)

        elif name == 'Annoy-o-Tron':
            instance = Minion(name, 1, 2, 2, type='Mech', taunt=True, bubble=True)
        elif name == 'Nightmare Amalgam':
            instance = Minion(name, 3, 4, 2, type='All')
        elif name == 'Shielded Minibot':
            instance = Minion(name, 2, 2, 2, type='Mech', bubble=True)

        elif name == 'Psych-o-Tron':
            instance = Minion(name, 3, 4, 3, type='Mech', taunt=True, bubble=True)
        
        return instance


class Heroes:
    @staticmethod
    def new(name, board):
        raise NotImplementedError
