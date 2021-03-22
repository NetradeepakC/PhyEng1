import math_2

# Circle class is a shape that represents a Circle in the 2D coordinate system.


class Class:

    default_mass = 1
    default_x = 0
    default_y = 0
    default_speedx = 0
    default_speedy = 0
    default_charge = 0

    def init(self, position=[default_x, default_y], velocity=[default_speedx, default_speedy], mass=default_mass, charge=default_charge):
        # initializing the Circle class with value.
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.charge = charge
