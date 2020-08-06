import pygame
import collections
import heapq
import numpy as np

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class SquareGraph:
    def __init__(self, cols, rows, g_set=None):
        self.cols = cols
        self.rows = rows
        self.g_set = g_set
        self.graph = [[0 for x in range(self.cols)] for y in range(self.rows)]
        self.start = self.g_set.start
        self.goal = self.g_set.goal
        self.walls = []
        self.boarder = []
        self.frontier = []
        self.visited = []
        self.path = []
        self.make_boarder()

    def make_boarder(self):
        for i, row in enumerate(self.graph):
            for j, item in enumerate(row):
                if (i == 0) or (i == self.rows - 1) or (j == 0) or (j == self.cols - 1):
                    self.graph[i][j] = 'b'
                    self.boarder.append((i, j))

    def construct_graph(self, start=None, goal=None, path=None):
        if start != None:
            self.graph[start[0]][start[1]] = 's'
        if goal != None:
            self.graph[goal[0]][goal[1]] = 'g'
        if path != None:
            self.path = path
            steps = 1
            for step in self.path[1:-1]:
                self.graph[step[0]][step[1]] = steps
                steps += 1
        else:     # Resets frontier and path back to empty space if maze is redone
            for i, row in enumerate(self.graph):
                for j, item in enumerate(row):
                    if (item == 'f') or (item == 'v') or (type(item) == int):
                        self.graph[i][j] = 0

    def add_wall(self, new_wall):
        self.walls.append(new_wall)
        self.graph[new_wall[0]][new_wall[1]] = 'w'

    def remove_wall(self, removed_wall):
        self.walls.remove(removed_wall)
        self.graph[removed_wall[0]][removed_wall[1]] = 0

    def add_frontier(self):
        for v in self.visited:
            if (self.graph[v[0]][v[1]] == 0) or (self.graph[v[0]][v[1]] == 'f'):
                self.graph[v[0]][v[1]] = 'v'
        for f in self.frontier:
            if (self.graph[f[0]][f[1]] == 0) or (self.graph[f[0]][f[1]] == 'v'):
                self.graph[f[0]][f[1]] = 'f'

    def in_graph(self, loc):
        (x, y) = loc
        return 0 <= x < self.cols and 0 <= y < self.rows

    def not_wall(self, loc):
        return loc not in self.walls

    def not_boarder(self, loc):
        return loc not in self.boarder

    def neighbors(self, loc):
        (x, y) = loc
        moves = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: moves.reverse()
        moves = filter(self.in_graph, moves)
        moves = filter(self.not_wall, moves)
        moves = filter(self.not_boarder, moves)
        return moves

    def update_grid(self, gameDisplay):
        gameDisplay.fill(self.g_set.BLACK)
        num_v = 10
        old = self.start
        for row_index, row in enumerate(self.graph):
            for col_index, item in enumerate(row):
                color = self.g_set.WHITE
                if item == 'w':
                    color = self.g_set.GREY
                elif item == 'b':
                    color = self.g_set.DARK_GREY
                elif item == 's':
                    color = self.g_set.GREEN
                elif item == 'g':
                    color = self.g_set.RED
                elif item == 'f':
                    color = self.g_set.ORANGE
                elif item == 'v':
                    if heuristic(old, self.goal) > heuristic((row_index, col_index), self.goal):
                        if num_v < 240 and num_v > 0:
                            num_v += 5
                    elif heuristic(old, self.goal, 'e') < heuristic((row_index, col_index), self.goal, 'e'):
                        if num_v < 240 and num_v > 0:
                            num_v -= 1
                    color = (255 - int(num_v / 4), num_v, 200 + int(num_v / 5))
                    old = (row_index, col_index)
                elif item > 0:
                    path = [val for row in self.graph for val in row if type(val) == int if val > 0]
                    step_tot = len(path)
                    step_left = step_tot - item
                    c = np.around(np.linspace(0, 150, step_tot), decimals=-1)
                    color = (150 - c[step_left], c[step_left], 0)

                pygame.draw.rect(gameDisplay,
                                 color,
                                 [(self.g_set.node_margin + self.g_set.node_width) * col_index + self.g_set.node_margin,
                                  (
                                              self.g_set.node_margin + self.g_set.node_height) * row_index + self.g_set.node_margin,
                                  self.g_set.node_width,
                                  self.g_set.node_height])
        return pygame.display.update()

    def reset_graph(self):
        self.graph = [[0 for x in range(self.cols)] for y in range(self.rows)]
        self.walls = []
        self.frontier = []
        self.visited = []
        self.path = []
        self.make_boarder()
        self.construct_graph(start=self.start, goal=self.goal)


class WeightedGraph(SquareGraph):
    def __init__(self, cols, rows, g_set=None):
        super().__init__(cols, rows, g_set)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


def heuristic(a, b, dist=None):
    (x1, y1) = a
    (x2, y2) = b
    if dist == None:      # Manhattan distance
        return abs(x1 - x2) + abs(y1 - y2)
    elif dist == 'e':    # Euclidean distance
        return np.around(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2), decimals=2)
