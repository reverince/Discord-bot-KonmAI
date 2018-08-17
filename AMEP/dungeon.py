import random
import time
from mob import *
from item import *


def generate_stage(cnt_stage, cnt_mob):
    ret = []
    random.seed(time.time())
    mob_stage = random.sample(list(range(cnt_stage)), cnt_mob)

    for i in range(cnt_stage):
        if i in mob_stage:
            ret.append(Skeleton())
        else:
            ret.append(MiniPotion())

    return ret


class Dungeon:

    def __init__(self, name, lvl, duration, cnt_stage, cnt_mob):
        self.name = name
        self.lvl = lvl
        self.duration = duration  # sec
        self.cnt_stage = cnt_stage
        self.cnt_mob = cnt_mob
        self.stages = generate_stage(cnt_stage, cnt_mob)

    def __str__(self):
        return self.name + '\n' + ', '.join([str(s) for s in self.stages])


#


class TestDungeon(Dungeon):
    
    def __init__(self):
        super().__init__("Test-Dungeon", 0, 300, 5, 4)
