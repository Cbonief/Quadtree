import pygame
import pygame.freetype

from Examples.Collision.particle import Particle
from Quadtree import Rectangle, Circle, Point, Quadtree
from util import random_zero_to_max, average


def run(window):
    timer = pygame.time.Clock()
    width = window.get_width()
    height = window.get_height()

    font = pygame.freetype.SysFont('Comic Sans MS', 18)

    boundary = Rectangle((0, 0), (width, height))

    particles = []

    using_quadtree = False
    for i in range(0, 200):
        particles.append(Particle([random_zero_to_max(width), random_zero_to_max(height)], 2))

    running = True
    frame_rate = []
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
