from Game.pisti_objects import *
from AI.ai import *

import pygame
import time
import os

class GameState:
    def __init__(self) -> None:
        self.p1 = Player()
        self.p2 = Player()
        self.deck = Deck()
        self.table = Table()
        self.round = 0
        self.game_ended = False;

        self.p1_to_play = False
        self.first_take = True
        self.hide_cards = True

        self.last_winner = self.p1

        self.save_dir = os.path.join("Output", str(time.time()))
        os.makedirs(self.save_dir)

    def initialize_game(self):
        self.deck.init_deck()
        self.table.init_state(self.deck)
        self.save_table()
        self.deal_new_cards()

    def reset_game(self):
        self.p1.hand.clear_hand()
        self.p1.reset_points()
        self.p2.hand.clear_hand()
        self.p2.reset_points()
        self.deck.clear_deck()
        self.table.clear_table()

        self.p1_to_play = False # always player starts
        self.first_take = True
        self.hide_cards = True

        self.round = 0
        self.game_ended = False

        self.save_dir = os.path.join("Output", str(time.time()))
        os.makedirs(self.save_dir)

    def deal_new_cards(self):
        self.p1.draw_cards(self.deck)
        self.p2.draw_cards(self.deck)
        self.save_draws()
        self.round += 1

    def play_card_handler(self, player, card):
        player.hand.remove_card(card)
        self.table.add_card(card)

    def is_ended(self):
        if self.deck.get_size() == 0 and self.p1.hand.get_size() == 0 and self.p2.hand.get_size() == 0:
            
            self.last_winner.points += self.table.evaluate_cards() # last winner gets residual cards
            self.last_winner.took_amount += self.table.get_size()

            if self.p1.took_amount > self.p2.took_amount:
                self.p1.points += 3
            elif self.p2.took_amount > self.p1.took_amount:
                self.p2.points += 3
            self.game_ended = True

            print("Game Ended!\n\nAI : {} - {} : Player".format(self.p1.points, self.p2.points))
        return self.game_ended
    
    def save_draws(self):
        filename = "tur{}.txt".format(self.round + 1)
        outfile = open(os.path.join(self.save_dir, filename), "w")
        outfile.write("Player 1 (AI)            --> " + str([str(card) for card in self.p1.hand.cards]) + "\n")
        outfile.write("Player 2 (Normal Player) --> " + str([str(card) for card in self.p2.hand.cards]) + "\n")
        outfile.close()

    def save_table(self):
        filename = "acilis.txt"
        outfile = open(os.path.join(self.save_dir, filename), "w")
        outfile.write("Cards on the Table       --> " + str([str(card) for card in self.table.cards]) + "\n")
        outfile.close()

class GameEngine:
    def __init__(self):
        self.game_state = GameState()
        self.ai = AI()

    def process_click(self, pos, cards_pos, cards_size):
        player_num, player = (1, self.game_state.p1) if self.game_state.p1_to_play else (2, self.game_state.p2)

        for i in range(4):
            rect = pygame.Rect(*cards_pos[(player_num, i + 1)], *cards_size)
            if (rect.collidepoint(pos) and player.hand.cards[i] != None):
                return player, player.hand.cards[i]
            
        return None, None

    def ai_play_card(self):
        self.play_card(self.game_state.p1, self.ai.generate_move())
        if self.game_state.table.is_taking():
            if self.game_state.first_take:
                self.game_state.hide_cards = False
                self.ai.update_information(self.game_state.table, False)
        self.recalculate_after_play(self.game_state.p1)

    def play_card(self, player, card):
        self.game_state.play_card_handler(player, card)
        self.ai.update_information(self.game_state.table, self.game_state.hide_cards)
    
    def recalculate_after_play(self, player):

        self.game_state.p1_to_play = not self.game_state.p1_to_play

        if self.game_state.table.is_taking():
            self.game_state.last_winner = player
            self.game_state.first_take = False

            player.points += self.game_state.table.evaluate_cards()
            player.took_amount += len(self.game_state.table.cards)
            self.game_state.table.clear_table()
        
        if self.game_state.is_ended():
            return

        if self.game_state.p1.hand.get_size() == 0 and self.game_state.p2.hand.get_size() == 0:
            self.game_state.deal_new_cards()

        self.ai.update_information(self.game_state.table, self.game_state.hide_cards)
