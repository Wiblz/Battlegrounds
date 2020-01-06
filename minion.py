class Minion:
    def __init__(self, name, attack, health, tier,
                type=None,
                summoned=False, 
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
        self.summoned = summoned
        
        self.taunt = taunt
        self.poison = False             # no poisonous minions by default
        self.bubble = bubble
        self.magnetic = magnetic
        self.cleave = cleave
        self.windfury = windfury

        self.effects = []               # minions that have effect applied to this minion

        self.deathrattles = []
        self.battlecry = None
        self.targeted_battlecry = None
        self.valid_targets = None
        self.add_effect = None          # aura effect this minion provides to other minions
                                        # (supposedly) should be function
        self.remove_effect = None
        self.on_play = None

        self.dead = False

    def __str__(self):
        return f'{self.name} {self.attack}/{self.health}'

    def __repr__(self):
        return self.__str__()

    def set_board(self, board):
        self.board = board
    
    def get_position(self):
        return self.board.minions.index(self)

    def hit(self, target):
        target.damage(self.damage, self.poison)
    
    def damage(self, amount, poison=False):
        if amount == 0:
            return
        
        if self.bubble:
            self.bubble = False
        else:
            self.health -= amount
            if poison or self.health <= 0:
                self.dead = True
