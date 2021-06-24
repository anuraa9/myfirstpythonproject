from random import randint


def x():
    print("From X")

    def y():
        print("from Y")

    return y()

x()
#
# SUITE = 'H D S C'.split()
# RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
#
#
# class Deck:
#     def __init__(self):
#         print("Creating New Ordered Deck!")
#         self.allcards = [(s, r) for s in SUITE for r in RANKS]
#
#     def shuffle(self):
#         print("Shuffling deck")
#         shuffle(self.allcards)
#
#     def split_in_half(self):
#         return (self.allcards[:26], self.allcards[26:])
#
#
# class Hand:
#     def __init__(self, cards):
#         self.cards = cards
#
#     def __str__(self):
#         print(f"Contains {self.cards} cards")
#
#     def add(self, added_cards):
#         self.cards.extend(added_cards)
#
#     def remove_card(self):
#         return self.cards.pop()
#
#
# class Player:
#     def __init__(self, name, hand):
#         self.name = name
#         self.hand = hand
#
#     def play_card(self):
#         drawn_card = self.hand.remove_card()
#         print(f"{self.name} has placed: {drawn_card}")
#         print("\n")
