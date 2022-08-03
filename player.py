aspects = ["little blind", "big blind", "dealer"]


class Player:
    def __init__(self, aspect, balance):
        self.hand = None
        self.folded = False
        self.bet_amount = 0
        self.aspect = aspect
        self.balance = balance

    def deal_cards(self, cards):
        self.hand = cards

    def set_aspect(self, aspect):
        self.aspect = aspect

    def bet(self, amount):
        self.bet_amount += amount
        self.balance -= amount

    def fold(self):
        self.hand = None
        self.bet_amount = 0
        self.folded = True


