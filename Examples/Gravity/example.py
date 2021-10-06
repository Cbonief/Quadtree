import pygame
import pygame.freetype
import sys

sys.path.append("C:\\Users\\carlo\\Code\\Quadtree")

from Examples.Gravity.body import Body, calculate_energy, ajust_speeds
from Quadtree import Rectangle, Circle, Point, Quadtree
from util import random_zero_to_max, average, random


def run(window):
    timer = pygame.time.Clock()
    width = window.get_width()
    height = window.get_height()

    font = pygame.freetype.SysFont('Comic Sans MS', 18)

    boundary = Rectangle((0, 0), (width, height))

    bodies = []

    using_quadtree = False
    for _ in range(0, 10):
        bodies.append(Body([random_zero_to_max(width), random_zero_to_max(height)], random(2,10)))
    _, _, total_energy = calculate_energy(bodies)
    running = True
    frame_rate = []
    while running:
        window.fill((0, 0, 0))
        dt = timer.tick()
        qtree = Quadtree(boundary, 4)

        for body in bodies:
            qtree.insert(Point([body.x[0], body.x[1]]))

        for body in bodies:
            if not body.highlight:
                if using_quadtree:
                    region = Circle([body.x[0], body.x[1]], body.r * 2 - 1)
                    others = qtree.query(region)
                    body.physics(others)
                else:
                    body.physics(bodies)
            body.render(window)
            body.move(dt)
        ajust_speeds(bodies, total_energy, 0.001, 1)

        if len(frame_rate) > 10:
            frame_rate.pop(0)
        frame_rate.append(1000/dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                using_quadtree = not using_quadtree

        if using_quadtree:
            text_render, _ = font.render('Using QuadTree', (255, 255, 255))
        else:
            text_render, _ = font.render('Not Using QuadTree', (255, 255, 255))
        rect = text_render.get_rect(center=(400 + 100 / 2, 300 + 20 / 2))
        window.blit(text_render, rect)
        text_render, _ = font.render('{} FPS'.format(round(average(frame_rate), 1)), (255, 255, 255))
        rect = text_render.get_rect(center=(400 + 100 / 2, 350 + 20 / 2))
        window.blit(text_render, rect)

        pygame.display.update()


if __name__ == "__main__":
    window = pygame.display.set_mode((600, 400))
    pygame.init()
    run(window)
