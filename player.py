aspects = ["little blind", "big blind", "dealer"]
btn_id_values = {
    0: "fold",
    1: "check",
    2: "raise",
    3: "call"
}


class Player:
    def __init__(self, aspect, balance):
        self.hand = []
        self.folded = False
        self.bet_amount = 0
        self.aspect = aspect
        self.balance = balance
        self.previous_bet = 0

    def deal_cards(self, cards):
        self.hand += cards

    def set_aspect(self, aspect):
        self.aspect = aspect

    def bet(self, amount):
        self.bet_amount += amount
        self.balance -= amount
        self.previous_bet = amount

    def fold(self):
        self.hand = None
        self.bet_amount = 0
        self.folded = True

    def win(self, amount):
        self.balance += amount

    def new_round_reset(self):
        self.hand = []
        self.folded = False
        self.bet_amount = 0

