import cards_client as cards


# function takes in a hand and returns an int equal to how good the hand is
# the order of value for hands is:
# royal flush > straight flush > four of a kind > full house > flush
# > straight > three of a kind > two pair > pair > high card
def determine_hand_value(hand: list) -> int:
    hand_counts = {
        "straight flush": [],
        "four of a kind": [],
        "full house": [],
        "flush": [],
        "straight": [],
        "three of a kind": [],
        "pair": [],
        "high_card": []
    }
    # get ranks and ranks with suits
    hand_ranks = []
    s_hand_ranks = []

    for i in hand:
        # find
        # pairs
        if cards.ranks[i.rank] in hand_ranks:
            # three of a kind
            if cards.ranks[i.rank] in hand_counts["pair"]:
                # four of a kind
                if cards.ranks[i.rank] in hand_counts["three of a kind"]:
                    hand_counts["four of a kind"].append(cards.ranks[i.rank])
                else:
                    hand_counts["three of a kind"].append(cards.ranks[i.rank])
            else:
                hand_counts["pair"].append(cards.ranks[i.rank])

        # add rank and suit to respective lists
        hand_ranks.append(cards.ranks[i.rank])
        s_hand_ranks.append([cards.ranks[i.rank], i.suit])

    # create a sorted hand
    s_hand_ranks = sorted(s_hand_ranks)

    # find the highest card
    hand_counts["high_card"].append(s_hand_ranks[-1][0])

    # find straights and flushes
    if len(hand) >= 5:
        streak = 0
        suit_match = True

        suit_counts = {
            "hearts": [0, 0],
            "diamonds": [0, 0],
            "spades": [0, 0],
            "clubs": [0, 0]
        }

        for i in range(0, len(hand)):
            # straight check section
            if streak == 4:
                # within hand_counts, only the highest card of the straight is stored
                hand_counts["straight"] = [s_hand_ranks[i][0]]

                # check for straight flush
                if suit_match:
                    hand_counts["straight flush"] = [s_hand_ranks[i][0]]

                streak -= 1
            # if current card is two and an ace exists
            if (i < len(hand) - 1) and (s_hand_ranks[i][0] == 1) and (s_hand_ranks[-1][0] == 13):
                streak += 1
                if not (s_hand_ranks[i][1] == s_hand_ranks[i + 1][1]):
                    suit_match = False
            # checks if the next highest card is one larger
            if (i < len(hand) - 1) and (s_hand_ranks[i][0] + 1 == s_hand_ranks[i + 1][0]):
                streak += 1
                if not (s_hand_ranks[i][1] == s_hand_ranks[i + 1][1]):
                    suit_match = False
            else:
                streak = 0
                suit_match = False

            # flush check section
            suit_counts[s_hand_ranks[i][1]][0] += 1
            suit_counts[s_hand_ranks[i][1]][1] = s_hand_ranks[i][0]

        # if there's a flush, add the highest card to hand_counts
        for i in suit_counts:
            if suit_counts[i][0] >= 5:
                hand_counts["flush"] = [suit_counts[i][1]]

    # check for full house
    if (len(hand_counts["three of a kind"]) >= 1) and (len(hand_counts["pair"]) >= 1):
        hand_counts["full house"] = [hand_counts["three of a kind"][0]]

    # RETURN POINTS
    hundreds = 700
    for i in hand_counts:
        if len(hand_counts[i]) == 1:
            return hundreds + hand_counts[i][0]
        if len(hand_counts[i]) > 1:
            highest = 0
            for q in hand_counts[i]:
                if q > highest:
                    highest = q
            if i == "pair":
                return hundreds + 50 + highest
            else:
                return hundreds + highest
        hundreds -= 100

    return 0
