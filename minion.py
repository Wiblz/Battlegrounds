class Minion:
    def __init__(self, name, attack, health, tier, type, taunt=False, bubble=False,
                       magnetic=False, battlecry=None, cleave=False):
        self.name = name
        self.attack = attack
        self.health = health
        self.tier = tier
        self.type = type
        
        self.taunt = taunt
        self.poison = False
        self.bubble = bubble
        self.magnetic = magnetic
        self.deathrattles = []
        self.battlecry = battlecry
        self.cleave = cleave


    def hit(self, target):
        return
        if self.bubble and target.attack != 0:
            self.bubble = False
