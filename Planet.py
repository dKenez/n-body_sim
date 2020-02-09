from math import sqrt


class Planet:
    """A class used to represent Planets."""
    __slots__ = ["name", "color", "mass", "center", "vel", "acc", "prev_acc", "radius"]

    def __init__(self, name, color="white", mass=1, center=None, vel=None):
        """Initialize the Planet object."""
        self.name = name
        self.color = color
        self.mass = mass if mass > 0 else 1
        self.center = [0, 0] if center is None else center
        self.vel = [0, 0] if vel is None else vel

        self.acc = [0, 0]
        self.prev_acc = [0, 0]
        self.radius = sqrt(mass)

    def clr_acc(self):
        """Clear the Planet's acceleration vector."""
        self.acc[0] = 0
        self.acc[1] = 0

    def apply_force(self, force):
        """Use the input force to calculate acceleration, and add it to the existing acceleration vector."""
        self.acc[0] += force[0] / self.mass
        self.acc[1] += force[1] / self.mass

    def update(self, delta_t):
        """Calculate the new position and velocity vectors using numerical integration."""
        for dim in (0, 1):
            xpp_2 = self.prev_acc[dim]
            xpp_1 = self.acc[dim]
            xp_1 = self.vel[dim]
            x_1 = self.center[dim]

            xp_0 = xp_1 + ((3 * xpp_1 - xpp_2) / 2) * delta_t
            x_0 = x_1 + ((xp_0 + xp_1) / 2) * delta_t
            self.prev_acc[dim] = xpp_1

            self.vel[dim] = xp_0
            self.center[dim] = x_0

    def update_r(self):
        """Update the radius of the Planet."""
        self.radius = sqrt(self.mass)
