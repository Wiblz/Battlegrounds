class Minion:
    def __init__(self, name, attack, health, tier,
                type=None, 
                taunt=False,
                bubble=False,
                magnetic=False,
                cleave=False,
                windfury=False):

        self.board = None
        self.hero = None
        self.position = None

        self.name = name
        self.attack = attack
        self.health = health
        self.tier = tier
        self.type = type
        
        self.taunt = taunt
        self.poison = False             # no poisonous minions by default
        self.bubble = bubble
        self.magnetic = magnetic
        self.cleave = cleave
        self.windfury = windfury

        self.effects = []               # minions that have effect applied to this minion

        self.deathrattles = []
        self.battlecry = None
        self.add_effect = None          # aura effect this minion provides to other minions
                                        # (supposedly) should be function
        self.remove_effect = None

        self.dead = False

    def set_board(self, board):
        self.board = board
    
    def get_position(self):
        return self.board.minions.index(self)
    
    def on_play(self, target=None):
        return
        # Handle battlecry
        if self.battlecry is not None:
            self.battlecry(self, self.board, target)
    
        # Add effect
        if self.add_effect is not None:
            self.add_effect(self.board)

    def on_death(self):
        return
        # Remove effect
        for minion in self.board.minions:
            if minion != self and self in minion.effects:
                minion.effects.remove(self)
                self.remove_effect(minion)

        # Handle deathrattles
        for deathrattle in self.deathrattles:
            deathrattle(self.board)


    # TODO: Deathrattles, effercts
    def hit(self, target, immune=False):
        if self.attack == 0:
            return
        
        # self -> target
        if target.bubble:
            target.bubble = False
        else:
            target.health -= self.attack
            if self.poison or target.health <= 0:
                target.dead = True
        
        # target -> self
        if not immune:          # 'workaround' for cleave damage
            if self.bubble:
                if target.attack != 0:
                    self.bubble = False
            else:
                self.health -= target.attack
                if target.poison or self.health <= 0:
                    self.dead = True
