import math
import random


class World():

    PLAYER_RADIUS = 5
    TURN_RADIUS = 10
    STEP = 1
    START_FOODS = 50
    WORLD_SIZE = (800, 800)
    
    WIDTH, HEIGHT = WORLD_SIZE
    TURN = 360 / ((TURN_RADIUS * math.pi) * STEP)

    def __init__(self, SEED=None):
        if SEED:
            random.seed(int(SEED))
        self.foods = []
        for _ in range(self.START_FOODS):
            self.foods.append(self._random_coords())
        self.player_x, self.player_y = self._random_coords()
        self.player_heading = random.randint(0, 359)

    def frame(self, input):
        self.player_heading = (self.player_heading + input * self.TURN) % 360
        heading_rads = math.radians(self.player_heading)
        self.player_x = (self.player_x + math.sin(heading_rads) * self.STEP) % self.WIDTH
        self.player_y = (self.player_y - math.cos(heading_rads) * self.STEP) % self.HEIGHT
        food_vectors = [((abs(self.player_x - x)), abs((self.player_y - y))) for x, y in self.foods]
        t_food_vectors = [(min(vector[0], self.WIDTH - vector[0]), min(vector[1], self.HEIGHT - vector[1])) for vector in food_vectors]
        food_distances = [self._vector_distance(vector) for vector in t_food_vectors]
        eaten = [index for index, distance in enumerate(food_distances) if distance < self.PLAYER_RADIUS]
        self.foods = [food for index, food in enumerate(self.foods) if index not in eaten]
        player_position = (int(round(self.player_x)), int(round(self.player_y)))
        try:
            nearest =  min([distance for index, distance in enumerate(food_distances) if index not in eaten])
            return nearest
        except:
            return None

    def _random_coords(self):
        return (random.randint(0, self.WIDTH - 1), random.randint(0, self.HEIGHT - 1))

    @staticmethod
    def _get_radius(area):
        return int(round(math.sqrt(area / math.pi)))

    @staticmethod
    def _vector_distance(vector):
        return math.sqrt(sum([v**2 for v in vector]))
