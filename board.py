# Your other murlocs have +2 attack
# Has +1 attack for each murlock on a battlefield
# Whenever a friendly beast dies
# Whenever you summon a mech
# Whenever you play a card with a battlecry
# Whenever your hero takes damage on your turn
# Whenever this minion takes damage
# Your cards that summon minions summon twice that many
# Whenever you summon a beast
# Your taunt minions have +2 attack
# Whenever a friendly demon dies
# After a friendly minion loses divine shield 
# After a friendly minion attacks
# At the end of your turn
# Whenever this minion takes damage
# Your minions trigger their deathrattles twice
# Your battlecries trigger twice
# Overkill
# Whenever a friendly mech dies
# Your other demons have +2/+2
# Whenever this attacks and kills minion
# This minion always attacks the enemy minion with the lowest attack

# After you play a demon

# + Windfury
# + At the start of each turn
# + Whenever you summon a murloc


class Board:
    def __init__(self):
        self.minions = []

        self.mechs = []
        self.murlocs = []
        self.demons = []
        self.beasts = []

        self.on_turn_start = []
        self.on_murloc_summoned = []
        self.on_demon_played = []

    def remove(self, minion):
        self.minions.remove(minion)

    def put(self, minion, slot):
        self.minions.insert(slot, minion)
        # TODO: handle alpha wolf
    
    def _trigger_all(self, minions):
        for minion in minions:
            minion.trigger()

    def _check_triggers(self, minion):
        if minion.on_play is not None:
            minion.on_play()
        
        if minion.type in ['murloc', 'all']:
            self._trigger_all(self.on_murloc_summoned)

        if minion.type in ['demon', 'all']:
            self._trigger_all(self.on_demon_played)

    def _register(self, minion):
        if minion.type in ['mech', 'all']:
            self.mechs.append(minion)
        
        elif minion.type in ['murloc', 'all']:
            self.murlocs.append(minion)

        elif minion.type in ['demon', 'all']:
            self.demons.append(minion)
        
        elif minion.type in ['beast', 'all']:
            self.beasts.append(minion)

    def play(self, minion, slot):
        self.put(minion, slot)
        
        if minion.battlecry is not None:
            minion.battlecry()

        self._check_triggers(minion)
        self._register(minion)

    def handle_targeted_battlecry(self, minion, target):
        minion.targeted_battlecry(target)
        self._check_triggers(minion)
        self._register(minion)
