
class Settings:
    """ ADD UPDATE SETTINGS FUNCTION """

    def __init__(self, alg=None):
        self.alg_type = alg

        self.smallfont = 20
        self.largefont = 40
        self.fonttype = 'comicsansms'

        # game_graphs settings
        self.node_width = 20
        self.node_height = 20
        self.node_margin = 5
        self.grid_width = 21
        self.grid_height = 21

        self.BLACK = (0, 0, 0)  # background
        self.WHITE = (255, 255, 255)  # empty ('0')
        self.DARK_GREY = (50, 50, 50)  # boarder ('b')
        self.GREY = (150, 150, 150)  # walls ('w')
        self.GREEN = (0, 180, 0)  # start ('s')
        self.RED = (180, 0, 0)  # goal ('g')
        self.BLUE = (0, 0, 200)  # path (int)
        self.BRIGHT_RED = (255, 0, 0)
        self.BRIGHT_GREEN = (0, 255, 0)
        self.YELLOW = (255, 235, 170)
        self.ORANGE = (230, 170, 40)

        # game settings
        self.running = True
        self.start = (1, int((self.grid_width - 1) / 2))
        self.goal = (self.grid_height - 2, int((self.grid_width - 1) / 2))

        # Pygame display setting
        self.display_width = (self.node_width * self.grid_width) + (self.node_margin * (1 + self.grid_width))
        self.display_height = (self.node_height * self.grid_height) + (self.node_margin * (1 + self.grid_height))



