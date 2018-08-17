HP, MP = 1, 2


class Item:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name


class Consumable(Item):

    def __init__(self, name, value, count):
        super().__init__(name, value)
        self.count = count


class Potion(Consumable):

    def __init__(self, name, value, count, purpose, amount):
        super().__init__(name, value, count)
        self.purpose = purpose
        self.amount = amount


#


class MiniPotion(Potion):

    def __init__(self):
        super().__init__("Mini-Potion", 10, 1, HP, 50)
