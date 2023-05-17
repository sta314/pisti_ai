import random
from Game.pisti_objects import *
from Game.pisti_game import *

class AI:
    def __init__(self):
        self.left_amount = 52
        self.num_freq = {cardnumber : 4 for cardnumber in CardNumbers}
    
    def initialize_ai(self, gamestate):
        self.hand = gamestate.p1.hand
        self.first_take = True
        self.last_played_card = None
        self.table_size = 0
        self.table_points = 0
        self.cards_left = gamestate.deck.cards.copy() + gamestate.p1.hand.cards.copy() + gamestate.p2.hand.cards.copy() + gamestate.table.cards.copy() # getting list of all (52) possible cards

    def reset_ai(self, gamestate):
        self.left_amount = 52
        self.num_freq = {cardnumber : 4 for cardnumber in CardNumbers}
        self.hand = gamestate.p1.hand
        self.first_take = True
        self.last_played_card = None
        self.table_size = 0
        self.table_points = 0
        self.cards_left = gamestate.deck.cards.copy() + gamestate.p1.hand.cards.copy() + gamestate.p2.hand.cards.copy() + gamestate.table.cards.copy() # getting list of all (52) possible cards

    # this is the main method that produces the next AI move using the information it has
    def generate_move(self):

        cards = list()
        for card in self.hand.cards:
            if card != None:
                cards.append(card)

        has_J = False
        for card in cards:
            if card.card_number == CardNumbers.J:
                has_J = True

        # finding the probabilities on each of the cards
        cards_proba = [self.get_number_proba(card.card_number) for card in cards]
        # arg-sorting those probabilities
        proba_sorted_idx = sorted(range(len(cards_proba)),key=cards_proba.__getitem__)

        card_numbers = [card.card_number for card in cards]

        # if can take, take
        if self.last_played_card != None and self.last_played_card.card_number in card_numbers:
            return cards[card_numbers.index(self.last_played_card.card_number)]
        
        # if have J
        if has_J:
            # if opponent doesnt have J
            if self.get_number_proba(CardNumbers.J) == 0:
                # play the cards impossible to take for maximizing the number of cards to take with J without risk 
                for i in range(len(cards)):
                    if cards[i].card_number != CardNumbers.J and cards_proba[i] == 0:
                        return cards[i]
                
            # if table has points on it, or table has greater size than 5, or it is the first take (for getting the information of hidden cards) play J
            if self.table_points > 0 or self.table_size > 6 or self.first_take:
                for i in range(len(cards)):
                    if cards[i].card_number == CardNumbers.J:
                        return cards[i]
                    
            # play the most played card, except J
            for i in range(len(cards)):
                card = cards[proba_sorted_idx[i]]
                if card.card_number != CardNumbers.J:
                    return card
                
        # if above exists dont work, play the most played card
        return cards[proba_sorted_idx[0]]

    # this is the only method that gets information about the game state
    def update_information(self, table, hide_first_cards):

        table_cards = table.cards

        self.first_take = hide_first_cards
        self.table_size = len(table_cards)
        self.last_played_card = table_cards[self.table_size - 1] if self.table_size > 0 else None
        self.table_points = table.evaluate_cards(hide_first_cards)

        # cards on the table
        for i in range(len(table_cards)):
            table_card = table_cards[i]

            # don't update information about hidden 3 cards at first
            if i <= 2 and hide_first_cards:
                continue

            if table_card in self.cards_left:
                self.remove_card(table_card)
        
        # cards on AI's hand
        for i in range(len(self.hand.cards)):
            hand_card = self.hand.cards[i]
            if hand_card != None:
                if hand_card in self.cards_left:
                    self.remove_card(hand_card)
    
    def remove_cards(self, cards):
        for card in cards:
            self.remove_card(card)

    def remove_card(self, card):
        self.cards_left.remove(card)
        self.num_freq[card.card_number] -= 1

    def get_number_proba(self, number):
         return self.num_freq[number] / self.left_amount