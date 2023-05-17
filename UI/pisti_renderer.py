from Game.pisti_objects import *
from Game.pisti_game import *

import pygame
import os

cards_path = os.path.join("Data", "Cards")

class Renderer():

    loaded_images = {}
    card_locations = {}

    card_size = (100, 140)
    table_center = (551, 268.5)

    def __init__(self):
        # Preloading cards
        for card_type in CardTypes.__members__:
            for card_number in [x.value for x in CardNumbers.__members__.values()]:
                identifier = (card_type, card_number)
                self.loaded_images[identifier] = pygame.image.load(os.path.join(cards_path,  "{}-{}.svg".format(card_type, card_number))).convert_alpha()
        self.loaded_images['back'] = pygame.image.load(os.path.join(cards_path, "back_r25.png")).convert_alpha()
        self.loaded_images['back'].set_colorkey((255, 255, 255))
        self.loaded_images['back'].set_alpha(128)

        for i in range(4):
            self.card_locations[(1, i + 1)] = (242.5 + 200 * i, 50)
            self.card_locations[(2, i + 1)] = (242.5 + 200 * i, 485)
        
    def render_background(self, window):
        window.blit(pygame.image.load(os.path.join("Data", "Board", "board.png")), (0, 0))

    def render_table(self, table, surf, hide_cards = False): # surf for now
        size = table.get_size()
        cards = table.cards

        left_bound = self.table_center[0] - 25 * (size/2)

        for i in range(size):
            card_info = None if (i <= 2 and hide_cards) else cards[i]
            surf.blit(self.render_card(card_info, pygame.Surface(self.card_size), True), (left_bound, self.table_center[1]))
            left_bound += 25

        # if len(cards) != 0:
        #     surf.blit(self.render_card(cards[len(cards) - 1], pygame.Surface(self.card_size), False), (left_bound, self.table_center[1]))

    def render_hands(self, hands, surf):
        for i in range(len(hands)):
            for j in range(len(hands[i].cards)):
                card = hands[i].cards[j]
                if card != None:
                    surf.blit(self.render_card(hands[i].cards[j], pygame.Surface(self.card_size), False), self.card_locations[(i + 1, j + 1)])
            
    def render_points(self, points, surf):
        font = pygame.font.SysFont(None, 60)

        p1_score_text = font.render(str(points[0]), True, (0, 0, 0))
        p1_score_text_rect = p1_score_text.get_rect(center=(112.5, 120))

        p2_score_text = font.render(str(points[1]), True, (0, 0, 0))
        p2_score_text_rect = p2_score_text.get_rect(center=(112.5, 555))

        surf.blit(p1_score_text, p1_score_text_rect)
        surf.blit(p2_score_text, p2_score_text_rect)

    def render_round(self, round, surf):
        font = pygame.font.SysFont(None, 32)

        p1_score_text = font.render("R" + str(round), True, (0, 0, 0))
        p1_score_text_rect = p1_score_text.get_rect(center=(590, 25))

        surf.blit(p1_score_text, p1_score_text_rect)

    def render_card(self, card, surf, fade = False):

        surf_rect = surf.get_rect()
        size = surf_rect.size
        # pygame.transform.smoothscale()
        
        idtf = card.get_identifier() if card != None else 'back'
        image = self.loaded_images[idtf]

        if image.get_size() != size:
            image = pygame.transform.smoothscale(image, size)
            self.loaded_images[idtf] = image
        
        surf.blit(image, (0, 0))

        return surf

    def render_endgame(self, surf):
        surf_rect = surf.get_rect()
        size = surf_rect.size

        downscaled_surf = pygame.transform.smoothscale(surf, (240, 450))
        upscaled_surf = pygame.transform.smoothscale(downscaled_surf, size)

        surf.fill(0)
        surf.blit(upscaled_surf, (0, 0))

        font = pygame.font.SysFont(None, 60)

        p1_score_text = font.render("Game ended. Press ESC to exit. Press any key to play again.", True, (255, 255, 255))
        p1_score_text_rect = p1_score_text.get_rect(center=surf_rect.center)

        temp = p1_score_text.copy()
        p1_score_text.fill((80, 80, 80, 100))
        p1_score_text.blit(temp, (0, 0))

        surf.blit(p1_score_text, p1_score_text_rect)