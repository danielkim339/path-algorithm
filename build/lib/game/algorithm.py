import pygame
import game_graphs as gr

class PathSearch:

    def __init__(self, g_set, alg, g):
        self.g_set = g_set
        self.start = self.g_set.start
        self.goal = self.g_set.goal
        self.alg = alg
        self.g = g
        self.current_front = None
        self.current_visit = None
        self.came_from = {}
        self.cost_so_far = {}
        self.path = []

        self.came_from[g_set.start] = None
        self.cost_so_far[g_set.start] = 0

        if self.alg == 'Breadth First Search':
            self.frontier = gr.Queue()
            self.frontier.put(self.start)
        else:
            self.frontier = gr.PriorityQueue()
            self.frontier.put(self.start, 0)

    def search_loop(self, gameDisplay):
        running = True
        finish = False
        self.g.update_grid(gameDisplay)

        while not self.frontier.empty() and running:
            current = self.frontier.get()
            self.current = current
            if current == self.goal:
                finish = True
                break
            elif self.alg == 'Breadth First Search':
                self.breadth_first_search()
            elif self.alg == 'Greedy Best First Search':
                self.greedy()
            elif self.alg == 'A* Search Algorithm':
                self.a_star()
            elif self.alg == "Dijkstra's Algorithm":
                self.dijkstras()
            self.g.frontier = self.current_front
            self.g.visited = self.current_visit
            self.g.add_frontier()

            if not finish:
                move = False
                while not move:
                    pygame.event.get()
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        finish = True
                        break
                    elif key[pygame.K_RIGHT]:
                        finish = False
                        move = True
                        self.g.update_grid(gameDisplay)
                    elif key[pygame.K_ESCAPE]:
                        self.g_set.running = False
                        running = False
                        break

        if self.frontier.empty() and self.current != self.goal:
            return False
        else:
            return True

    def breadth_first_search(self):
        for n in self.g.neighbors(self.current):
            if n not in self.came_from:
                self.frontier.put(n)
                self.came_from[n] = self.current
        self.current_front = list(self.frontier.elements)
        self.current_visit = list(set(key for key in self.came_from))

    def greedy(self):
        for n in self.g.neighbors(self.current):
            if n not in self.came_from:
                priority = gr.heuristic(self.goal, n)
                self.frontier.put(n, priority)
                self.came_from[n] = self.current
        self.current_front = [item[1] for item in self.frontier.elements]
        self.current_visit = list(set(key for key in self.came_from))

    def dijkstras(self):
        for n in self.g.neighbors(self.current):
            new_cost = self.cost_so_far[self.current] + self.g.cost(self.current, n)
            if n not in self.cost_so_far or new_cost < self.cost_so_far[n]:
                self.cost_so_far[n] = new_cost
                priority = new_cost
                self.frontier.put(n, priority)
                self.came_from[n] = self.current
        self.current_front = [item[1] for item in self.frontier.elements]
        self.current_visit = list(set(key for key in self.came_from))

    def a_star(self):
        for n in self.g.neighbors(self.current):
            new_cost = self.cost_so_far[self.current] + self.g.cost(self.current, n)
            if n not in self.cost_so_far or new_cost < self.cost_so_far[n]:
                self.cost_so_far[n] = new_cost
                priority = new_cost + gr.heuristic(self.goal, n)
                self.frontier.put(n, priority)
                self.came_from[n] = self.current
        self.current_front = [item[1] for item in self.frontier.elements]
        self.current_visit = list(set(key for key in self.came_from))

    def construct_path(self):
        path_loc = self.goal
        path = []
        while path_loc != self.start:
            path.append(path_loc)
            path_loc = self.came_from[path_loc]
        path.append(self.start)
        path.reverse()
        self.path = path
        return path
