import numpy as np
from minion import Minion
from recruitment import RecruitmentStage

a = RecruitmentStage(np.random.default_rng())
opt = a.generate_recruitment_options(3)
print(opt)

while True:
    input()
    opt = a.refresh(opt, 3)
    print(opt)

# list = []

# a = Minion('test', 1, 1, 1)
# list.append(a)
# b = Minion('test', 1, 1, 1)
# list.append(b)

# print(list.index(a), list.index(b))
