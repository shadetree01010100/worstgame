import math
import random
import pygame


class Player():

    TURN_DEG = 30
    STEP = 1
    PLAYER_RADIUS = 5

    def __init__(self, world, coordinates):
        self.world = world
        self.coordinates = coordinates
        self.direction = random.uniform(0, 360)
        self.last_move = 0

    def move(self, direction=0):
        self.last_move = direction
        self.direction = (self.direction + direction * self.TURN_DEG) % 360
        heading_rads = math.radians(self.direction)
        x, y = self.coordinates
        self.coordinates = (
            (x + math.sin(heading_rads) * self.STEP) % self.world.WIDTH,
            (y - math.cos(heading_rads) * self.STEP) % self.world.HEIGHT
        )
        self._consume_foods()

    def closest_food(self):
        min_distance = self.world.WIDTH * self.world.HEIGHT
        for coordinates in self.world.foods:
            distance = self._distance(coordinates)
            min_distance = min(min_distance, distance)
        return min_distance

    def _consume_foods(self):
        remaining_foods = []
        for coordinates in self.world.foods:
            distance = self._distance(coordinates)
            if distance > self.PLAYER_RADIUS:
                remaining_foods.append(coordinates)
        self.world.foods = remaining_foods

    def _distance(self, coordinates):
        delta_x = abs(self.coordinates[0] - coordinates[0])
        delta_y = abs(self.coordinates[1] - coordinates[1])
        vector = (
            min(delta_x,
                self.world.WIDTH / 2 - abs(self.world.WIDTH / 2 - delta_x)),
            min(delta_y,
                self.world.HEIGHT / 2 - abs(self.world.HEIGHT / 2 - delta_y))
        )
        distance = math.sqrt(sum([v**2 for v in vector]))
        return distance


class World():

    START_FOODS = 50
    WIDTH = 800
    HEIGHT = 800
    EPISODE_LIMIT = 100000

    def __init__(self, WINDOW_TITLE='', SEED=None, RENDER=True):
        self.RENDER = RENDER
        if SEED != None:
            random.seed(SEED)
        self.episodes = 0
        self.player = Player(self, self._random_coords())
        self.foods = []
        for _ in range(self.START_FOODS):
            self.foods.append(self._random_coords())
        if self.RENDER:
            pygame.init()
            pygame.font.init()
            self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption(WINDOW_TITLE)
            self.font = pygame.font.Font(None, 30)
            self._draw_world()

    def episode(self, input):
        self.episodes += 1
        self.player.move(input)

    def done(self):
        if not self.foods or self.episodes == self.EPISODE_LIMIT:
            if self.RENDER:
                pygame.display.quit()
            return True
        if self.RENDER and self.episodes % self.RENDER == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return True
            self._draw_world()
        return not bool(self.foods)

    def _draw_world(self):
        self.surface.fill((0, 0, 0))
        for food in self.foods:
            self._draw_food(food)
        self._draw_player()
        self._draw_stats()
        pygame.display.update()

    def _draw_food(self, position, color=(0, 255, 0)):
        x, y = position
        pygame.draw.line(self.surface, color, (x, y - 2), (x, y + 2))
        pygame.draw.line(self.surface, color, (x - 2, y), (x + 2, y))

    def _draw_player(self, color=(255, 255, 255)):
        position = (
            int(round(self.player.coordinates[0])),
            int(round(self.player.coordinates[1])))
        radius = self.player.PLAYER_RADIUS
        pygame.draw.circle(self.surface, color, position, radius)

    def _draw_stats(self, color=(255, 255, 255)):
        elapsed = self.font.render('{}'.format(self.episodes), 0, color)
        remain = self.font.render('{}'.format(len(self.foods)), 0, color)
        ep_in = self.font.render(
            '{}'.format(round(self.player.last_move, 2)), 0, color)
        ep_out = self.font.render(
            '{}'.format(round(self.player.closest_food(), 1)), 0, color)
        self.surface.blit(elapsed, (1, 0))
        self.surface.blit(remain, (1, 16))
        self.surface.blit(ep_in, (1, 32))
        self.surface.blit(ep_out, (1, 48))

    def _random_coords(self):
        return (
            random.uniform(0, self.WIDTH),
            random.uniform(0, self.HEIGHT))


if __name__ == "__main__":
    WORLD = World()
    while not input("press enter to continue"):
        WORLD.episode(0)
