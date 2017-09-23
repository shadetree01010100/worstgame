import math
import random
import pygame


class World():

    START_FOODS = 50
    WIDTH = 800
    HEIGHT = 800
    RENDER = False

    PLAYER_RADIUS = 5
    TURN_DEG = 5
    STEP = 1

    def __init__(self, SEED=None):
        if SEED:
            random.seed(int(SEED))
        if self.RENDER:
            pygame.init()
            pygame.font.init()
            self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption('window title goes here')
            self.font = pygame.font.Font(None, 30)
            self.clock = pygame.time.Clock()
        self.episodes = 0
        self.foods = []
        for _ in range(self.START_FOODS):
            self.foods.append(self._random_coords())
        self.player_x, self.player_y = self._random_coords()
        self.player_heading = random.randint(0, 359)

    def episode(self, input):
        self.episodes += 1
        self.player_heading = (
            self.player_heading + input * self.TURN_DEG) % 360
        heading_rads = math.radians(self.player_heading)
        self.player_x = (
            self.player_x + math.sin(heading_rads) * self.STEP) % self.WIDTH
        self.player_y = (
            self.player_y - math.cos(heading_rads) * self.STEP) % self.HEIGHT
        food_vectors = []
        remaining_foods = []
        food_distances = []
        for x, y in self.foods:
            vector = (
                min(abs(self.player_x - x), self.WIDTH - x),
                min(abs(self.player_y - y), self.HEIGHT - y))
            distance = self._distance(vector)
            if distance > self.PLAYER_RADIUS:
                food_vectors.append(vector)
                remaining_foods.append((x, y))
                food_distances.append(distance)
        if not remaining_foods:
            if self.RENDER:
                pygame.quit()
            return None
        self.foods = remaining_foods
        if self.RENDER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
            self.surface.fill((0, 0, 0))
            self.draw_player()
            for food in self.foods:
                self.draw_food(food)
            self.draw_stats()
            pygame.display.update()
            self.clock.tick(0)
        return min(food_distances)

    def draw_player(self, color=(255, 255, 255)):
        position = (int(round(self.player_x)), int(round(self.player_y)))
        pygame.draw.circle(self.surface, color, position, self.PLAYER_RADIUS)

    def draw_food(self, position, color=(0, 255, 0)):
        x, y = position
        pygame.draw.line(self.surface, color, (x, y - 2), (x, y + 2))
        pygame.draw.line(self.surface, color, (x - 2, y), (x + 2, y))

    def draw_stats(self, color=(255, 255, 255)):
        elapsed_ep = self.font.render(str(self.episodes), False, color)
        remaining = self.font.render(str(len(self.foods)), False, color)
        self.surface.blit(elapsed_ep, (1, 0))
        self.surface.blit(remaining, (1, 16))

    def _random_coords(self):
        return (
            random.randint(0, self.WIDTH - 1),
            random.randint(0, self.HEIGHT - 1))

    @staticmethod
    def _distance(vector):
        return math.sqrt(sum([v**2 for v in vector]))
