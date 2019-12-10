class Hand:
    def __init__(self):
        self.minions = []   # minions in the hand are stored as strings
        self.counters = dict()

    def buy(self, minion_name):
        self.minions.append(minion_name)
        if minion_name not in self.counters:
            self.counters[minion_name] = 0

        self.counters[minion_name] += 1

    # TODO: create instance, register listeners
    def play(self, minion_name):
        pass