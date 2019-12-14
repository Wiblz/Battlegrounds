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

        self.on_turn_start = []
        self.on_murloc_summoned = []
        self.on_demon_played = []
