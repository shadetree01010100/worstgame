import math
import random
import pygame


class World():

    PLAYER_RADIUS = 5
    TURN_RADIUS = 10
    STEP = 1
    START_FOODS = 50
    WORLD_SIZE = (800, 800)
    RENDER = False

    _WIDTH, _HEIGHT = WORLD_SIZE
    _TURN = 360 / ((TURN_RADIUS * math.pi) * STEP)

    def __init__(self, SEED=None):
        if SEED:
            random.seed(int(SEED))
        if self.RENDER:
            pygame.init()
            pygame.font.init()
            surface = pygame.display.set_mode(self.WORLD_SIZE)
            pygame.display.set_caption('window title goes here')
            default_font = pygame.font.Font(None, 30)
        self.foods = []
        for _ in range(self.START_FOODS):
            self.foods.append(self._random_coords())
        self.player_x, self.player_y = self._random_coords()
        self.player_heading = random.randint(0, 359)

    def frame(self, input):
        self.player_heading = (self.player_heading + input * self._TURN) % 360
        heading_rads = math.radians(self.player_heading)
        self.player_x = (
            self.player_x + math.sin(heading_rads) * self.STEP) % self._WIDTH
        self.player_y = (
            self.player_y - math.cos(heading_rads) * self.STEP) % self._HEIGHT
        food_vectors = []
        for x, y in self.foods:
            vector = (
                min(abs(self.player_x - x), self._WIDTH - x),
                min(abs(self.player_y - y), self._HEIGHT - y))
            food_vectors.append(vector)
        food_distances = [self._distance(vector) for vector in food_vectors]
        remaining_foods = []
        for index, distance in enumerate(food_distances):
            if distance > self.PLAYER_RADIUS:
                remaining_foods.append(self.foods[index])
        if not remaining_foods:
            return None
        self.foods = remaining_foods
        return min(food_distances)

    def _random_coords(self):
        return (
            random.randint(0, self._WIDTH - 1),
            random.randint(0, self._HEIGHT - 1))

    @staticmethod
    def _distance(vector):
        return math.sqrt(sum([v**2 for v in vector]))
