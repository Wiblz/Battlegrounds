from minion import Minion
import random

# Your other murlocs have +2 attack
# Has +1 attack for each murlock on a battlefield
# Whenever you summon a mech
# Whenever you play a card with a battlecry
# Whenever your hero takes damage on your turn
# Whenever this minion takes damage
# Your cards that summon minions summon twice that many
# Whenever you summon a beast
# Your taunt minions have +2 attack
# Whenever a friendly demon dies
# After a friendly minion loses divine shield 
# At the end of your turn
# Whenever this minion takes damage
# Your minions trigger their deathrattles twice
# Your battlecries trigger twice
# Overkill
# Whenever a friendly mech dies
# Your other demons have +2/+2
# Whenever this attacks and kills minion
# This minion always attacks the enemy minion with the lowest attack


# + Windfury

# + At the start of each turn
# + After a friendly minion attacks

# + Whenever you summon a murloc

# + After you play a demon

# + Whenever a friendly beast dies


class Board:
    def __init__(self):
        self.minions = []

        self.mechs = []
        self.murlocs = []
        self.demons = []
        self.beasts = []

        self.on_turn_start = []
        self.on_minion_attack = []

        self.on_murloc_summoned = []
        self.on_demon_played = []
        self.on_beast_died = []

        self.pogos_played = 0

    def full(self):
        return len(self.minions) == 7

    def remove(self, minion):
        self.minions.remove(minion)

    def put(self, minion, slot):
        self.minions.insert(slot, minion)
        # TODO: handle alpha wolf
    
    def get_random(self):
        return random.choice(self.minions)

    def _trigger_all(self, minions):
        for minion in minions:
            print('trigger')
            minion.trigger()

    def _check_for_deaths(self, minions):
        for minion in minions:
            if minion.dead:
                self.on_death(minion)

    def _check_on_death_triggers(self, minion):
        if minion.type in ['Beast', 'All']:
            self._trigger_all(self.on_beast_died)

    def _check_on_summon_triggers(self, minion):
        if minion.type in ['Murloc', 'All']:
            self._trigger_all(self.on_murloc_summoned)

    def _check_on_play_triggers(self, minion):
        if minion.type in ['Demon', 'All']:
            self._trigger_all(self.on_demon_played)
        
        self._check_on_summon_triggers(minion)             # playing minion also triggers 'on summon' events

    def _register(self, minion):
        if minion.on_play is not None:
            minion.on_play()

        if minion.type in ['Mech', 'All']:
            self.mechs.append(minion)
        
        elif minion.type in ['Murloc', 'All']:
            self.murlocs.append(minion)

        elif minion.type in ['Demon', 'All']:
            self.demons.append(minion)
        
        elif minion.type in ['Beast', 'All']:
            self.beasts.append(minion)

    def play(self, minion, slot):
        self.put(minion, slot)
        
        if minion.battlecry is not None:
            summoned = minion.battlecry()
            for minion in summoned:
                self._check_on_summon_triggers(minion)

        self._check_on_play_triggers(minion)
        self._register(minion)

    def on_death(self, dead_minion):
        # Remove effect
        for minion in self.minions:
            if minion != dead_minion and dead_minion in minion.effects:
                minion.effects.remove(dead_minion)
                dead_minion.remove_effect(minion)

        # Handle deathrattles
        for deathrattle in dead_minion.deathrattles:
            position = dead_minion.get_position()
            self.remove(dead_minion)
            dead_minion.deathrattle(self, position)

    def handle_targeted_battlecry(self, minion, target):
        minion.targeted_battlecry(target)
        self._check_on_play_triggers(minion)
        self._register(minion)

    def hit(self, attacking:Minion, target:Minion):
        attacking.hit(target)
        target.hit(attacking)

        for minion in self.on_minion_attack:
            minion.trigger()
        
        self._check_for_deaths([target, attacking])

    def damage(self, target, amount):
        target.damage(amount)
        self._check_for_deaths([target, attacking])
