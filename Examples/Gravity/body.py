import numpy as np
from pygame import draw

DENSITY = 0.01
MAX_INITIAL_VELOCITY = 0.001
G = 0.2

class Body:
    def __init__(self, position, radius):
        self.x = np.array(position)
        self.highlight = False
        self.r = radius
        self.m = DENSITY*self.r**2
        self.v = MAX_INITIAL_VELOCITY*np.array([2*np.random.rand()-1, 2*np.random.rand()-1])
        self.vabs = np.linalg.norm(self.v)
        self.a = np.array([0, 0])


    def move(self, dt):
        self.v += self.a*dt
        self.x += self.v*dt
        self.vabs = np.linalg.norm(self.v)
        self.highlight = False
    
    def calculate_gravitational_acceleration(self, others):
        self.a *= 0
        for other in others:
            if self != other:
                r3 = np.linalg.norm(self.x-other.x)**3
                a = (G*other.m/r3)*(other.x-self.x)
                self.a += a
                

    def render(self, window):
        if self.highlight:
            draw.circle(window, (255, 255, 0), (self.x[0], self.x[1]), self.r)
        else:
            draw.circle(window, (255, 255, 255), (self.x[0], self.x[1]), self.r)

    def physics(self, others):
        self.a = np.array([0.0, 0.0])
        for other in others:
            if self != other:
                distance = np.linalg.norm(self.x-other.x)
                distance_squared = distance**2
                r3 = distance**3
                direction = (other.x-self.x)
                a = (G*other.m/r3)*direction
                self.a += a
                if distance_squared + 1 < (other.r + self.r)**2:
                    # overlap = (other.r + self.r)-distance
                    # self.x -= direction*(overlap/2)/distance
                    # other.x += direction*(overlap/2)/distance
                    self.v = self.v + (2*other.m/(self.m+other.m))*np.dot(self.v-other.v, self.x-other.x)*(direction)/distance_squared
                    other.v = other.v - (2*self.m/(self.m+other.m))*np.dot(self.v-other.v, self.x-other.x)*(direction)/distance_squared
                    self.v = self.v * 0.8
                    other.v = other.v * 0.8
                    self.vabs = np.linalg.norm(self.v)
                    other.vabs = np.linalg.norm(other.v)
                    self.highlight = True
                    other.highlight = True

def calculate_energy(bodies):
    kinectic = 0
    potential = 0
    for i in range(len(bodies)):
        kinectic += bodies[i].m*bodies[i].vabs**2/2
        for j in range(i, len(bodies)-1):
            if(i != j):
                r = np.linalg.norm(bodies[i].x-bodies[j].x)
                potential -= G*bodies[i].m*bodies[j].m/r
    return kinectic, potential, kinectic+potential

def ajust_speeds(bodies, total_energy, ratio=1e-6, iterations=2):
    for i in range(0, iterations):
        velocities = np.array([bodie.vabs for bodie in bodies])
        print(velocities)
        masses = np.array([bodie.m for bodie in bodies])
        _, _, calculated_energy = calculate_energy(bodies)
        error = total_energy-calculated_energy
        velocities += 2*ratio*error*np.dot(velocities, masses)
        print(velocities)
        for i in range(len(bodies)):
            bodies[i].v = bodies[i].v*velocities[i]/bodies[i].vabs
            print(velocities[i]/bodies[i].vabs)
            bodies[i].vabs = velocities[i]


