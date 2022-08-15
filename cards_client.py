import random
import player
import calculations
import socket

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

#connect to host
host = input("Enter the host IP: ")
port = 62222
c = socket.socket()
c.connect((host,port))

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

        self.players = []
        for i in range(0, num_players):
            if i <= 1:
                self.players.append(player.Player(player.aspects[i], stack))
            else:
                self.players.append(player.Player(None, stack))
        self.players.append(player.Player(player.aspects[2], stack))

    def add_to_river(self, amount):
        self.river += list(self.deck[0:amount])
        for i in range(0, amount):
            self.deck.pop(0)

    def add_bet(self, amount, player_num):
        self.players[player_num].bet(amount)
        self.pot += amount

    def deal_to_player(self, player_num, amount):
        j = 0
        #recieve and split up the data
        data = c.recv(1024)
        data = str(data, 'utf-8')
        data = data.split(";")

        #go through all the players and sync card data
        for k in range(0, player_num):
            for i in range(0, amount):
                #store the data
                data1 = data[j]
                data1 = str(data1)
                data2 = data[j+1]
                data2 = str(data2)

                #create a new card object
                card = Card(data2, data1)

                #remove the used data from the data array
                data.pop(0)
                data.pop(0)

                #deal the new card objects
                self.players[k].deal_cards([card])

    def determine_winner(self):
        previous_highest = [0, None]
        for i in self.players:
            q = calculations.determine_hand_value(i.hand + self.river)
            if q > previous_highest[0]:
                previous_highest[0] = q
                previous_highest[1] = i

        previous_highest[1].win(self.pot)


class Card:
    # create the card, using the input suit and rank
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
