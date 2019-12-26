from tawern_data import options_count, tier_contents, count_per_minion, minions
import numpy as np


class Pool:
    def __init__(self, generator):
        self.generator = generator
        self.pool = dict()
        self.tier_sum = {
            1 : 216,
            2 : 240,
            3 : 221,
        }

        for tier in tier_contents:
            self.pool[tier] = dict()
            cnt = count_per_minion[tier]

            for minion in tier_contents[tier]:
                self.pool[tier][minion] = cnt
    
    def return_minions(self, options):
        for option in options:
            self.pool[minions[option]['tier']][option] += 1

    def generate_minions(self, tier, size=None):
        size = size or options_count[tier]
        active_pool = []
        probabilities = np.array([])

        for t in range(1, tier + 1):
            active_pool += list(self.pool[t].keys())
            probabilities = np.concatenate((probabilities, np.array(list(self.pool[t].values()))))

        probabilities /= probabilities.sum()
        options = self.generator.choice(np.array(active_pool), size=size, p=probabilities)
        
        for option in options:
            self.pool[minions[option]['tier']][option] -= 1

        return options