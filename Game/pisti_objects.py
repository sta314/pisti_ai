import random
from enum import Enum

class CardTypes(Enum):
    heart = 1
    diamond = 2
    spade = 3
    club = 4

class CardNumbers(Enum):
    A = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    J = 11
    Q = 12
    K = 13


class Card:
    def __init__(self, card_type, card_number):
        self.card_type = card_type
        self.card_number = card_number

    def get_identifier(self):
        return (self.card_type.name, self.card_number.value)

    def __str__(self):
        return f"{self.card_type.name}, {self.card_number.name}";

class Player:
    def __init__(self):
        self.hand = Hand()
        self.points = 0
        self.took_amount = 0

    def reset_points(self):
        self.points = 0
        self.took_amount = 0

    def draw_cards(self, deck):
        self.hand.cards.clear()
        drawn_cards = deck.draw_cards(4)
        self.hand.add_cards(drawn_cards)

class Hand:
    def __init__(self):
        self.cards = list() # max length of 4

    def add_cards(self, card):
        self.cards.extend(card)

    def remove_card(self, card):
        self.cards[self.cards.index(card)] = None
        return card
    
    def clear_hand(self):
        self.cards.clear()

    def get_size(self):
        return sum(x is not None for x in self.cards)

class Deck:
    def __init__(self):
        self.cards = list()

    def init_deck(self):
        for i in range(1, 5):
            for j in range(1, 14):
                self.cards.append(Card(CardTypes(i), CardNumbers(j)))

    def clear_deck(self):
        self.cards.clear()

    def draw_cards(self, amount = 1):
        drawn_cards = list()
        for i in range(amount):
            random_card = self.cards.pop(random.randrange(len(self.cards)))
            drawn_cards.append(random_card)
        if amount > 1:
            return drawn_cards
        else:
            return random_card
        
    def get_size(self):
        return len(self.cards)
        
class Table:
    def __init__(self):
        self.cards = list()
    
    def init_state(self, deck):
        self.cards.clear()
        self.cards.extend(deck.draw_cards(4))

    def get_size(self):
        return len(self.cards)
    
    def is_taking(self):
        size = self.get_size()
        return size >= 2 and ((self.cards[size - 1].card_number == self.cards[size - 2].card_number) 
                or 
                (self.cards[size - 1].card_number == CardNumbers.J))
    
    def evaluate_cards(self, skip_first_cards = False):
        points = 0
        skip_n_cards = 0 if not skip_first_cards else 3
        for card in self.cards:
            if skip_n_cards > 0:
                skip_n_cards -= 1
                continue
            if card.card_type == CardTypes.diamond and card.card_number == CardNumbers._10:
                points += 3
            elif card.card_type == CardTypes.club and card.card_number == CardNumbers._2:
                points += 2
            elif card.card_number == CardNumbers.J or card.card_number == CardNumbers.A:
                points += 1
        if self.get_size() == 2 and self.cards[0].card_number == self.cards[1].card_number:
            points += 10
        return points

    def add_card(self, card):
        self.cards.append(card)

    def clear_table(self):
        self.cards.clear()

