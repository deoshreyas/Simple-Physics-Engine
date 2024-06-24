import pygame 
from pygame.locals import * 
import engine 
from random import randint

pygame.init()

# Set up the window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Physics Engine")

# Set up the constraints for our bodies 
constraint_pos = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
constraint_radius = 300

RADIUS = 50
noOfBodies = 100

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bodies to simulate
bodies = []

# Solver for our Physics Engine 
class Solver:
    gravity = (0, 0.1)

    def update(self):
        self.applyGravity()
        self.applyConstraint()
        self.solveCollisions()
        self.updatePosition()

    def updatePosition(self):
        for body in bodies:
            body.updatePosition()
    
    def applyGravity(self):
        for body in bodies:
            body.accelerate(self.gravity)
    
    def applyConstraint(self):
        for body in bodies:
            to_obj = engine.subtract_vectors(body.position_current, constraint_pos)
            dist = engine.compute_length(to_obj)
            if dist > constraint_radius - RADIUS:
                n = (to_obj[0] / dist, to_obj[1] / dist)
                corrected_position = (constraint_pos[0] + n[0] * (constraint_radius - RADIUS),
                                      constraint_pos[1] + n[1] * (constraint_radius - RADIUS))
                body.position_current = corrected_position
    
    def solveCollisions(self):
        noOfBodies = len(bodies)
        for i in range(noOfBodies):
            body1 = bodies[i]
            for j in range(i+1, noOfBodies):
                body2 = bodies[j]
                collision_axis = engine.subtract_vectors(body1.position_current, body2.position_current)
                distance = engine.compute_length(collision_axis)
                if distance<RADIUS*2:
                    n = (collision_axis[0]/distance, collision_axis[1]/distance)
                    delta = RADIUS*2 - distance 
                    body1.position_current = engine.add_vectors(body1.position_current, (5*n[0]*delta, 5*n[1]*delta))
                    body2.position_current = engine.subtract_vectors(body2.position_current, (5*n[0]*delta, 5*n[1]*delta))

# Main function 
enginePhysicsSolver = Solver()
def main():
    global colour 

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        # Add bodies ever 0.1 seconds
        if pygame.time.get_ticks() % 10 == 0 and len(bodies) < noOfBodies:
            bodies.append(engine.VerletObject((400, 400), (400, 400), (0, 0)))

        # Draw the constraint circle boundaries 
        pygame.draw.circle(screen, BLACK, constraint_pos, constraint_radius, 1)
        
        # Update the physics 
        enginePhysicsSolver.update()

        # Draw the bodies
        for body in bodies:
            pygame.draw.circle(screen, BLACK, (int(body.position_current[0]), int(body.position_current[1])), RADIUS)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()