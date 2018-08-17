# 무희 7, 아이템 21 : A2고서, B2대나무피리, C2춤부채, D3삼현금, E3종이우산, F4차세트, G5벚꽃머리핀
# 액션 토큰 4x2 : 1. 1장 뒤집어 배치 / 2. 2장 비공개 제외 / 3. 3장 공개, 상대 1장 선택 선물, 자신 2장 선물 / 4. 2+2장 공개, 상대 한 묶음 선택 선물 / 자신 나머지 선물
# 승리조건 : (라운드 종료 시) 11점 > 4무희


class HanamiCard:
    TYPES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    POINTS = [2, 2, 2, 3, 3, 4, 5]
    MAIKOS = ['무1', '무2', '무3', '무4', '무5', '무6', '무7']
    ITEMS = ['고서', '대나무 피리', '춤부채', '삼현금', '종이우산', '차 세트', '벚꽃 머리핀']

    def __init__(self, type, point, name):
        self.type = type
        self.point = point
        self.name = name

    def __str__(self):
        return self.type + str(self.point) + ' ' + self.name

    @classmethod
    def str(cls, cards):
        return [str(card) for card in cards]


class HanamiDeck:
    def __init__(self):
        self.cards = []
        for i in range(7):
            for p in range(HanamiCard.POINTS[i]):
                self.cards.append(HanamiCard(HanamiCard.TYPES[i], HanamiCard.POINTS[i], HanamiCard.ITEMS[i]))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()


class HanamiMaiko:
    def __init__(self, type, point, name):
        self.type = type
        self.point = point
        self.name = name

    def __str__(self):
        return self.type + str(self.point) + ' ' + self.name


class HanamiPlayer:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.actions = [1, 2, 3, 4]


class Hanamikoji:
    def __init__(self, player1, player2):
        self.p1 = HanamiPlayer(player1)
        self.p2 = HanamiPlayer(player2)
        self.round = 1
        self.turn = player1
        self.maikos = []
        for i in range(7):
            self.maikos.append(HanamiCard(HanamiCard.TYPES[i], HanamiCard.POINTS[i], HanamiCard.MAIKOS[i]))
        self.round_init()

    def __str__(self):
        return '{}\n{} : {}\n{} : {}'.format('\n'.join([str(maiko) for maiko in self.maikos]), self.p1.name, ', '.join(HanamiCard.str(self.p1.cards)), self.p2.name, ', '.join(HanamiCard.str(self.p2.cards)))

    def card_init(self):
        self.p1.cards = [self.deck.draw(), self.deck.draw(), self.deck.draw(), self.deck.draw(), self.deck.draw(), self.deck.draw()]
        self.p2.cards = [self.deck.draw(), self.deck.draw(), self.deck.draw(), self.deck.draw(), self.deck.draw(), self.deck.draw()]

    def action_init(self):
        self.p1.actions = [1, 2, 3, 4]
        self.p2.actions = [1, 2, 3, 4]

    def round_init(self):
        self.deck = HanamiDeck()
        self.deck.shuffle()
        self.card_init()
        self.action_init()
