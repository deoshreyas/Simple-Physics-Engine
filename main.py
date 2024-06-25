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

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bodies to simulate
bodies = []

# Generate colours 
def genCol(last_col):
    r, g, b = last_col
    step = 10  # Adjust the color transition speed
    if r == 255 and g < 255 and b == 0: 
        g += step
    elif g == 255 and r > 0 and b == 0:  
        r -= step
    elif g == 255 and b < 255 and r == 0:
        b += step
    elif b == 255 and g > 0 and r == 0:  
        g -= step
    elif b == 255 and r < 255 and g == 0:
        r += step
    elif r == 255 and b > 0 and g == 0:
        b -= step
    else:
        r, g, b = 255, 0, 0
    # Ensure RGB components are within the 0-255 range
    r, g, b = min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b))
    return (r, g, b)

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
            if dist > constraint_radius - body.radius:
                n = (to_obj[0] / dist, to_obj[1] / dist)
                corrected_position = (constraint_pos[0] + n[0] * (constraint_radius - body.radius),
                                      constraint_pos[1] + n[1] * (constraint_radius - body.radius))
                body.position_current = corrected_position
    
    def solveCollisions(self):
        noOfBodies = len(bodies)
        for i in range(noOfBodies):
            body1 = bodies[i]
            for j in range(i+1, noOfBodies):
                body2 = bodies[j]
                collision_axis = engine.subtract_vectors(body1.position_current, body2.position_current)
                distance = engine.compute_length(collision_axis)
                min_dist = body1.radius + body2.radius
                if distance<min_dist:
                    n = (collision_axis[0]/distance, collision_axis[1]/distance)
                    delta = min_dist - distance 
                    body1.position_current = engine.add_vectors(body1.position_current, (0.5*n[0]*delta, 0.5*n[1]*delta))
                    body2.position_current = engine.subtract_vectors(body2.position_current, (0.5*n[0]*delta, 0.5*n[1]*delta))

# Main function 
enginePhysicsSolver = Solver()
colour = (255, 0, 0)
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
        
        # Add bodies 
        if pygame.mouse.get_pressed()[0]:
            pygame.time.delay(100)
            pos = pygame.mouse.get_pos()
            if engine.compute_length(engine.subtract_vectors(pos, constraint_pos)) < constraint_radius:
                bodies.append(engine.VerletObject(pos, pos, (0, 0), randint(10, 25), colour))
                colour = genCol(colour)

        # Draw the constraint circle boundaries 
        pygame.draw.circle(screen, BLACK, constraint_pos, constraint_radius, 1)
        
        # Update the physics 
        enginePhysicsSolver.update()

        # Draw the bodies
        for body in bodies:
            pygame.draw.circle(screen, body.colour, (int(body.position_current[0]), int(body.position_current[1])), body.radius)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()