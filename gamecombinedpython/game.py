# Imports for python file (.py)
import pygame
import game_graphs as gr
import game_settings as gs
import algorithm as algorithm

# Imports for JupyterLab notebook file (.ipynb)
# import pygame
# import ipynb.fs.full.game_graphs as gr
# import ipynb.fs.full.game_settings as gs
# import ipynb.fs.full.algorithm as algorithm


def quit_game(g_set, g, gameDisplay):
    g_set.running = False
    pygame.quit()
    quit()


def text_objects(text, font, g_set):
    textSurface = font.render(text, True, g_set.WHITE)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, g_set, g, gameDisplay, action=None, alg_pick='dij'):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            g_set.alg_type = alg_pick  ##########################
            return action(g_set, g, gameDisplay)

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont(g_set.fonttype, g_set.smallfont)
    # textSurf, textRect = text_objects(msg, smallText)
    textSurf, textRect = text_objects(msg, smallText, g_set)

    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def clicked_node(g_set):
    pos = pygame.mouse.get_pos()
    row = pos[1] // (g_set.node_height + g_set.node_margin)
    col = pos[0] // (g_set.node_width + g_set.node_margin)
    return row, col


""" Main game functions. """


def menu(g_set, g, gameDisplay):
    while g_set.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                g_set.running = False
                return  # quit_game(g_set, g, gameDisplay)

        gameDisplay.fill(g_set.BLACK)
        largeText = pygame.font.SysFont(g_set.fonttype, g_set.largefont)
        smallText = pygame.font.SysFont(g_set.fonttype, g_set.smallfont)

        textSurf1, textRect1 = text_objects('Pathfinder Visualization', largeText, g_set)
        textSurf2, textRect2 = text_objects('1. "CLICK" to add/remove walls. "ENTER" to start search.', smallText,
                                            g_set)
        textSurf3, textRect3 = text_objects('2. "RIGHT" to visualize search process. "SPACE" jump to result', smallText,
                                            g_set)
        textRect1.center = ((g_set.display_width / 2), (g_set.display_height / 5))
        textRect2.center = ((g_set.display_width / 2), (g_set.display_height / 4))
        textRect3.center = ((g_set.display_width / 2), (g_set.display_height / 3))

        gameDisplay.blits(blit_sequence=((textSurf1, textRect1), (textSurf2, textRect2), (textSurf3, textRect3)))

        # button("Start", 40,200,80,25, g_set.GREEN, g_set.BRIGHT_GREEN, g_set, g, gameDisplay, game_loop)
        # button("Quit", 160,200,80,25, g_set.RED, g_set.BRIGHT_RED, g_set, g, gameDisplay, quit_game)

        button("   Breadth First Search   ", 60, 200, 160, 40, g_set.GREEN, g_set.BRIGHT_GREEN, g_set, g, gameDisplay,
               game_loop, 'bfs')
        button("   Dijkstra's Algorithm   ", 300, 200, 160, 40, g_set.GREEN, g_set.BRIGHT_GREEN, g_set, g, gameDisplay,
               game_loop, 'dij')
        button("    A* Search Algorithm   ", 60, 300, 160, 40, g_set.GREEN, g_set.BRIGHT_GREEN, g_set, g, gameDisplay,
               game_loop, 'astar')
        button(" Greedy Best First Search ", 300, 300, 160, 40, g_set.GREEN, g_set.BRIGHT_GREEN, g_set, g, gameDisplay,
               game_loop, 'greedy')
        button(" Quit ", 60, 400, 400, 40, g_set.RED, g_set.BRIGHT_RED, g_set, g, gameDisplay, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop(g_set, g, gameDisplay):
    while g_set.running:
        start_search = False
        mouse_click = False
        old_r, old_c = 0, 0
        g.update_grid(gameDisplay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                g_set.running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    g.construct_graph()
                    start_search = True
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click = False

            while (mouse_click and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION)):
                pygame.event.pump()
                button = pygame.mouse.get_pressed()
                if button[0] == False:
                    break

                row, col = clicked_node(g_set)

                if row != old_r or col != old_c:
                    if g.graph[row][col] == 'w':
                        g.remove_wall((row, col))
                    elif (g.graph[row][col] != 's') and (g.graph[row][col] != 'g') and (
                            g.graph[row][col] != 'b'):  # Prevent wall replacing start/goal
                        g.add_wall((row, col))
                    old_r, old_c = row, col

                g.construct_graph()
                g.update_grid(gameDisplay)

        if not g_set.running:
            return

        elif start_search and g_set.running:
            results = algorithm.PathSearch(g_set, g_set.alg_type, g)
            valid_path = results.search_loop(gameDisplay)

            if not valid_path:
                pygame.display.set_caption('Dead end. Try again.')
                g.reset_graph()
                results.g.reset_graph()  # need both???
                game_loop(g_set, g, gameDisplay)

            else:
                path = results.construct_path()
                g.construct_graph(path=path)
                pygame.display.set_caption("Search Results")
                # g.update_grid(gameDisplay)
                results.g.update_grid(gameDisplay)

        # pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    g_set = gs.Settings()

    start = g_set.start
    goal = g_set.goal
    g = gr.WeightedGraph(g_set.grid_width, g_set.grid_height,
                         g_set)  # g = gr.SquareGraph(g_set.grid_width, g_set.grid_height, g_set)
    g.construct_graph(start=start, goal=goal)

    gameDisplay = pygame.display.set_mode((g_set.display_width, g_set.display_height))
    pygame.display.set_caption('Pathfinder')
    gameDisplay.fill(g_set.BLACK)
    clock = pygame.time.Clock()

    while g_set.running:
        menu(g_set, g, gameDisplay)
        game_loop(g_set, g, gameDisplay)

    pygame.quit()
    quit()
