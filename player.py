aspects = ["dealer", "little blind", "big blind"]


class Player:
    def __init__(self, aspect, balance):
        self.hand = None
        self.aspect = aspect
        self.balance = balance

    def change_balance(self, amount):
        self.balance += amount

    def deal_cards(self, cards):
        self.hand = cards

    def set_aspect(self, aspect):
        self.aspect = aspect

