import random
import player
import calculations
suits = ["hearts", "diamonds", "spades", "clubs"]
ranks = {
    "two": 1,
    "three": 2,
    "four": 3,
    "five": 4,
    "six": 5,
    "seven": 6,
    "eight": 7,
    "nine": 8,
    "ten": 9,
    "jack": 10,
    "queen": 11,
    "king": 12,
    "ace": 13
}


def reset_deck():
    deck_ = []
    for i in suits:
        for q in ranks:
            deck_.append(Card(i, q))

    random.shuffle(deck_)

    return deck_


class GameState:
    def __init__(self, stack, little_blind, num_players):
        self.pot = 0
        self.deck = reset_deck()
        self.little_blind = little_blind
        self.num_players = num_players
        self.river = []
        self.current_highest_bet = 0

        self.players = []
        for i in range(0, num_players):
            if i <= 1:
                self.players.append(player.Player(player.aspects[i], stack))
            else:
                self.players.append(player.Player(None, stack))
        self.players.append(player.Player(player.aspects[2], stack))

    def add_to_river(self, amount):
        self.river += list(self.deck[0:amount])
        for i in range(0, amount + 1):
            self.deck.pop(0)

    def add_bet(self, amount, player_num):
        if amount <= self.players[player_num].balance:
            self.players[player_num].bet(amount)
            self.pot += amount

            if self.current_highest_bet < self.players[player_num].bet_amount:
                self.current_highest_bet = self.players[player_num].bet_amount

        else:
            amount = self.players[player_num].balance
            if amount == 0:
                self.players[player_num].fold()
            self.players[player_num].bet(amount)
            self.pot += amount

            if self.current_highest_bet < self.players[player_num].bet_amount:
                self.current_highest_bet = self.players[player_num].bet_amount

    def deal_to_player(self, player_num, amount):
        for i in range(0, amount):
            self.players[player_num].deal_cards([self.deck[0]])
            self.deck.pop(0)

    def get_call_amount(self, player_num):
        return self.current_highest_bet - self.players[player_num].bet_amount

    def select_player_option(self, player_num, option_num, amount=50):
        if option_num == 0:
            self.players[player_num].fold()
        elif option_num == 1:
            self.add_bet(self.get_call_amount(player_num), player_num)
        elif option_num == 2:
            self.add_bet(amount + self.get_call_amount(player_num), player_num)
        else:
            print("invalid option number")

    def determine_winner(self):
        previous_highest = [0, None]
        for i in self.players:
            if not i.folded:
                q = calculations.determine_hand_value(i.hand + self.river)
                if q > previous_highest[0]:
                    previous_highest[0] = q
                    previous_highest[1] = i

        previous_highest[1].win(self.pot)
        print(f"Player {previous_highest[1]} wins a pot of value ${self.pot} with a score of {previous_highest[0]}")

    def new_round_reset(self):
        self.pot = 0
        self.current_highest_bet = 0
        self.deck = reset_deck()
        self.river = []

        for i in self.players:
            i.new_round_reset()


class Card:
    # create the card, using the input suit and rank
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
