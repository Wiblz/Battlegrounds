from abc import ABC


# TODO: put the name and the cost in this class
class Card(ABC):
    name = None
    cost = None
    def __repr__(self):
        return self.name

class MinionCard(Card):
    def __init__(self, name):
        self.cost = 0
        self.name = name
        self.attack_buff = 0
        self.health_buff = 0

    def __repr__(self):
        if self.attack_buff != 0 or self.health_buff != 0:
            return super.__repr__() + f' (+{self.attack_buff}/{self.health_buff})'
        else:
            return super.__repr__()
    
class RecruitmentMap(Card):
    def __init__(self, cost, tier):
        self.cost = 3
        self.tier = tier
        self.name = f'Recruitment map (tier {tier})'

class Coin(Card):
    def __init__(self):
        self.cost = -1        # adds one gold when used
        self.name = 'Coin'
