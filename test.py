import numpy as np
from recruitment import RecruitmentStage

a = RecruitmentStage()
opt = a.generate_options(3)
print(opt)

while True:
    input()
    opt = a.refresh(opt, 3)
    print(opt)