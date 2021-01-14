import pygame

from Examples.Collision.particle import Particle
from Quadtree import Rectangle, Circle, Point, Quadtree
from util import random_zero_to_max


def run(window):
    timer = pygame.time.Clock()
    width = window.get_width()
    height = window.get_height()
    boundary = Rectangle((0, 0), (width, height))

    particles = []

    using_quadtree = False
    for i in range(0, 200):
        particles.append(Particle([random_zero_to_max(width), random_zero_to_max(height)], 2))

    running = True
    while running:
        window.fill((0, 0, 0))
        dt = timer.tick()
        qtree = Quadtree(boundary, 4)

        for particle in particles:
            qtree.insert(particle)

        for particle in particles:
            if not particle.highlight:
                if using_quadtree:
                    region = Circle([particle.x, particle.y], particle.r * 2 - 1)
                    others = qtree.query(region)
                    particle.check_collision(others)
                else:
                    particle.check_collision(particles)
            particle.render(window)
            particle.move(width, height)

        frame_rate = (1000/dt)
        print(frame_rate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                using_quadtree = not using_quadtree

        pygame.display.update()


if __name__ == "__main__":
    window = pygame.display.set_mode((600, 400))
    pygame.init()
    run(window)
