class Character:

    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def __str__(self):
        return self.name

    def is_dead(self):
        return self.hp <= 0


class Puppet(Character):

    def __init__(self, name, hp, atk):
        super().__init__(name, hp, atk)
        self.lvl = 0
        self.exp = 0


class Enemy(Character):

    def __init__(self, name, hp, atk, exp):
        super().__init__(name, hp, atk)
        self.exp = exp


#


class TestPuppet(Puppet):
    cnt = 0

    def __init__(self):
        TestPuppet.cnt += 1
        super().__init__("Testroid" + str(TestPuppet.cnt), 100, 30)


class Skeleton(Enemy):
    
    def __init__(self):
        super().__init__("Skeleton", 100, 10, 10)
