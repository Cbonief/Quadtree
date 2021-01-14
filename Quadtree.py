import pygame


class Point:
    def __init__(self, position, data=None):
        self.x = position[0]
        self.y = position[1]
        self.data = None


class Rectangle:
    def __init__(self, position, size):
        self.x = position[0]
        self.y = position[1]
        self.w = size[0]
        self.h = size[1]

    def contains(self, point):
        return self.x - self.w <= point.x <= self.x + self.w and self.y - self.h <= point.y <= self.y + self.h

    def intersects(self, region):
        return not (region.x - region.w > self.x + self.w or
                    region.x + region.w < self.x - self.w or
                    region.y - region.h > self.y + self.h or
                    region.y + region.h < self.y - self.h)


class Circle:
    def __init__(self, position, radius):
        self.x = position[0]
        self.y = position[1]
        self.r = radius
        self.rSquared = self.r * self.r

    def contains(self, point):
        distance_squared = (point.x - self.x) ** 2 + (point.y - self.y) ** 2
        return distance_squared <= self.rSquared

    def intersects(self, region):
        x_dist = abs(region.x - self.x)
        y_dist = abs(region.y - self.y)

        r = self.r

        w = region.w
        h = region.h

        edges = (x_dist - w)*(x_dist - w) + (y_dist - h)*(y_dist - h)

        if x_dist > (r + w) or y_dist > (r + h):
            return False

        if x_dist <= w or y_dist <= h:
            return True

        return edges <= self.rSquared


class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None
        self.divided = False

    def query(self, region):
        found = []
        if not region.intersects(self.boundary):
            return found

        if self.divided:
            found.extend(self.northwest.query(region))
            found.extend(self.northeast.query(region))
            found.extend(self.southwest.query(region))
            found.extend(self.southeast.query(region))
        else:
            for point in self.points:
                if region.contains(point):
                    found.append(point)

        return found

    # Creates four
    def subdivide(self):
        self.divided = True

        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        nw = Rectangle((x + w, y - h), (w, h))
        ne = Rectangle((x - w, y - h), (w, h))
        sw = Rectangle((x + w, y + h), (w, h))
        se = Rectangle((x - w, y + h), (w, h))

        self.northwest = Quadtree(nw, self.capacity)
        self.northeast = Quadtree(ne, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)

        for point in self.points:
            self.insert(point)

        self.points = []

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        if self.northwest.insert(point):
            return True
        elif self.northeast.insert(point):
            return True
        elif self.southwest.insert(point):
            return True
        elif self.southeast.insert(point):
            return True
