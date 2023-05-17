import pygame
from UI.pisti_renderer import *
from AI.ai import *


pygame.init()
window = pygame.display.set_mode((1200, 675))
pygame.display.set_caption("Pisti")

renderer = Renderer()
gameengine = GameEngine()
gamestate = gameengine.game_state

gamestate.initialize_game()
gameengine.ai.initialize_ai(gamestate)
gameengine.ai.update_information(gamestate.table, gamestate.hide_cards)

run = True
while(run):

    sleep = 0
    is_valid_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            else:
                if gamestate.game_ended:
                    gamestate.reset_game()
                    gamestate.initialize_game()
                    gameengine.ai.reset_ai(gamestate)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                player, player_card = gameengine.process_click(pos, renderer.card_locations, renderer.card_size)
                if player != None:
                    is_valid_click = True
                    
    is_taking = False
    if is_valid_click:
        gameengine.play_card(player, player_card)
        is_taking = gamestate.table.is_taking()
        if gamestate.first_take and is_taking and player == gamestate.p2:
            gamestate.hide_cards = False
            sleep += 1000

    if gamestate.hide_cards and not gamestate.first_take:
        gamestate.hide_cards = False

    window.fill(0)

    renderer.render_background(window)
    renderer.render_table(gamestate.table, window, gamestate.hide_cards)
    renderer.render_hands([gamestate.p1.hand, gamestate.p2.hand], window)
    renderer.render_points([gamestate.p1.points, gamestate.p2.points], window)
    renderer.render_round(gamestate.round, window)
    
    if gamestate.game_ended:
        renderer.render_endgame(window)

    if is_valid_click:
        gameengine.recalculate_after_play(player)
        sleep += 500

    pygame.display.flip()

    # pygame.time.wait(sleep)

    if not gamestate.game_ended:
        if gamestate.p1_to_play:
            gameengine.ai_play_card()
            pygame.time.wait(500)