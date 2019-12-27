from card import MinionCard


# TODO: make subscriptable (?)
class Hand:
    def __init__(self):
        self.cards = []
        self.counters = dict()

    def size(self):
        return len(self.cards)
    
    def is_full(self):
        return self.size() >= 10
    
    def is_empty(self):
        return self.size() == 0

    def buy(self, minion_name):
        self.cards.append(MinionCard(minion_name))
        if minion_name not in self.counters:
            self.counters[minion_name] = 0

        self.counters[minion_name] += 1

    # TODO: create instance, register listeners
    def play(self, minion_name):
        pass