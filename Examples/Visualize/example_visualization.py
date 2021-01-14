import pygame
from Quadtree import Rectangle, Circle, Point, Quadtree
from util import random_zero_to_max


def run(window):

    boundary = Rectangle((300, 200), (300, 200))
    quadtree = Quadtree(boundary, 6)

    points = []
    for i in range(0, 100):
        random_point = Point((random_zero_to_max(599), random_zero_to_max(399)))
        points.append(random_point)
        quadtree.insert(random_point)

    running = True
    radius = 100
    while running:
        window.fill((0, 0, 0))
        show(quadtree, window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    if radius < 150:
                        radius += 10
                elif event.y == -1:
                    if radius > 50:
                        radius -= 10

        mouse_position = pygame.mouse.get_pos()
        points_in_range = quadtree.query(Circle(mouse_position, radius))

        pygame.draw.circle(window, (0, 255, 0), (mouse_position[0], mouse_position[1]), radius, width=1)
        for point in points:
            pygame.draw.circle(window, (255, 0, 0), (point.x, point.y), 2)

        for point in points_in_range:
            pygame.draw.circle(window, (0, 255, 0), (point.x, point.y), 2)

        pygame.display.update()


def show(qtree, window):
    pygame.draw.rect(window, (255, 255, 255), (qtree.boundary.x - qtree.boundary.w, qtree.boundary.y - qtree.boundary.h, 2 * qtree.boundary.w , 2 * qtree.boundary.h), width=1)
    if qtree.divided:
        show(qtree.northwest, window)
        show(qtree.northeast, window)
        show(qtree.southwest, window)
        show(qtree.southeast, window)


if __name__ == "__main__":
    window = pygame.display.set_mode((600, 400))
    pygame.init()
    run(window)
