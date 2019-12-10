import numpy as np
from tawern_data import *


class RecruitmentStage:
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

    def on_buy(self, name):
        pass

    def on_sell(self, minion):
        pass

    def refresh(self, previous_options, tier):
        for option in previous_options:
            self.pool[minions[option]['tier']][option] += 1
        
        return self.generate_options(tier)

    def generate_options(self, tier):
        active_pool = []
        probabilities = np.array([])

        for t in range(1, tier + 1):
            active_pool += list(self.pool[t].keys())
            probabilities = np.concatenate((probabilities, np.array(list(self.pool[t].values()))))

        probabilities /= probabilities.sum()
        options = self.generator.choice(np.array(active_pool), size=options_count[tier], p=probabilities)
        
        for option in options:
            self.pool[minions[option]['tier']][option] -= 1

        return options
