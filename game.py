import datetime
import math
import random
import pygame


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

FPS = 0
WIDTH = 800
HEIGHT = 800
STEP = 1
TURN_RADIUS = 10
_TURN = 360 / (TURN_RADIUS * math.pi)
START_FOODS = 50
FRAME_LIMIT = 100000

pygame.init()
pygame.font.init()

world = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('this game blows lol')
default_font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

def draw_player(position, area=100, color=white):
    radius = int(round(math.sqrt(area / math.pi)))
    pygame.draw.circle(world, color, position, radius)

def draw_pixel(position, color=green):
    pygame.draw.line(
        world,
        color,
        (position[0], position[1] - 2),
        (position[0], position[1] + 2))
    pygame.draw.line(
        world,
        color,
        (position[0] - 2, position[1]),
        (position[0] + 2, position[1]))

# def draw_vector(start, stop, color=white):
    # pygame.draw.line(world, color, start, stop)

def draw_radar(position, distance):
    pygame.draw.circle(world, green, position, max(distance, 1), 1)

def draw_score():
    score = default_font.render(str(elapsed_frames), False, white)
    remain = default_font.render(str(len(foods)), False, white)
    world.blit(score, (1, 0))
    world.blit(remain, (1, 16))

def vector_distance(vector):
    return math.sqrt(sum([v**2 for v in vector]))

def random_coords():
    return (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))

foods = []
for _ in range(START_FOODS):
    foods.append(random_coords())

player_x, player_y = random_coords()
player_heading = random.randint(0, 359)

print('\tpress [esc] or [Q] to quit')
running = True
elapsed_frames = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print('\twindow closed')
            break
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                running = False
                print('\tuser exit')
                break
            elif event.key == pygame.K_LEFT:
                player_heading = (player_heading - _TURN) % 360
            elif event.key == pygame.K_RIGHT:
                player_heading = (player_heading + _TURN) % 360
    if elapsed_frames == FRAME_LIMIT:
        running = False
        print('\tfucking fail')
        break
    heading_rads = math.radians(player_heading)
    player_x = (player_x + math.sin(heading_rads) * STEP) % WIDTH
    player_y = (player_y - math.cos(heading_rads) * STEP) % HEIGHT
    # # # coordinate deltas between player and each food
    food_vectors = [
        ((abs(player_x - x)), abs((player_y - y))) for x, y in foods]
    # # # this world is a "hypercylinder:" both axes loop back to themselves.
    # # # a point is never further than half the dimension,
    # # # so we find the shortest distance to each food considering we can 
    # # # circumvent the world on either axis
    t_food_vectors = [
        (min(vector[0], WIDTH - vector[0]),
        min(vector[1], HEIGHT - vector[1])) for vector in food_vectors]
    food_distances = [vector_distance(vector) for vector in t_food_vectors]
    # nearest = [
        # foods[index] for index, vector in enumerate(t_food_vectors) \
            # if vector_distance(vector) == min(food_distances)]
    sensed_radius = [
        vector_distance(vector) for vector in t_food_vectors \
            if vector_distance(vector) == min(food_distances)]
    player_position = (int(round(player_x)), int(round(player_y)))
    world.fill(black)
    draw_player(player_position)
    for food in foods:
        draw_pixel(food)
    # for coords in nearest:
        # draw_vector(player_position, coords)
    draw_radar(player_position, int(round(min(sensed_radius))))
    elapsed_frames += 1
    draw_score()
    pygame.display.update()
    if FPS:
        clock.tick(FPS)
print('\t{} food left after {} frames'.format(len(foods), elapsed_frames))
pygame.quit()
