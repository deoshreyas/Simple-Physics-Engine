from math import sqrt

def add_vectors(v1, v2):
    """Add two vectors."""
    return (v1[0] + v2[0], v1[1] + v2[1])

def subtract_vectors(v1, v2):
    """Subtract two vectors."""
    return (v1[0] - v2[0], v1[1] - v2[1])

def compute_length(vector):
    """Compute the length (magnitude) of a 2D vector."""
    x, y = vector
    return sqrt(x**2 + y**2)

class VerletObject:
    def __init__(self, position_current, position_old, acceleration):
        self.position_current = position_current
        self.position_old = position_old
        self.acceleration = acceleration
    
    def updatePosition(self):
        VELOCITY = subtract_vectors(self.position_current, self.position_old)
        # Save current position
        self.position_old = self.position_current
        # Perform Verlet Integration 
        # self.position_current += self.position_current + VELOCITY + self.acceleration
        self.position_current = add_vectors(add_vectors(self.position_current, VELOCITY), self.acceleration)
        # Reset acceleration 
        self.acceleration = (0, 0)
    
    def accelerate(self, acc):
        self.acceleration = add_vectors(self.acceleration, acc)