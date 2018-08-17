class Player:

    def __init__(self, name):
        self.name = name
        self.puppets = []
        self.silver = 100
        self.manade = 100

    def __str__(self):
        return self.name

    def info(self):
        return "[{}]\t{}\t인형 {}개 | 은화 {}sv | 마네이드 {}ml".format(self.puppets_level(), self.name, len(self.puppets), self.silver, self.manade)

    def puppets_level(self):
        return sum(list(map(lambda x: x.lvl, self.puppets)))

    def puppets_name(self):
        return [str(p) for p in self.puppets]
