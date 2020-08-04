import pygame
from game import menu, game_loop
from game_settings import Settings
import game_graphs as gr

pygame.init()
pygame.font.init()
g_set = Settings()
start, goal = g_set.start, g_set.goal
g = gr.WeightedGraph(g_set.grid_width, g_set.grid_height, g_set)
g.construct_graph(start=start, goal=goal)
gameDisplay = pygame.display.set_mode((g_set.display_width, g_set.display_height))
gameDisplay.fill(g_set.BLACK)

while g_set.running:
    menu(g_set, g, gameDisplay)
    game_loop(g_set, g, gameDisplay)

pygame.quit()
quit()