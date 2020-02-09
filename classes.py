from math import sqrt


class Planet:
    __slots__ = ["name", "color", "mass", "center", "vel", "acc", "prev_acc", "radius"]

    def __init__(self, name, color="white", mass=1, center=None, vel=None, acc=None, ):
        self.name = name
        self.mass = mass if mass > 0 else 1
        self.center = [0, 0] if center is None else center
        self.vel = [0, 0] if vel is None else vel
        self.acc = [0, 0] if acc is None else acc
        self.color = color

        self.prev_acc = [0, 0]
        self.radius = int(sqrt(mass))

    def clr_acc(self):
        self.acc[0] = 0
        self.acc[1] = 0

    def apply_force(self, force):
        self.acc[0] += force[0] / self.mass
        self.acc[1] += force[1] / self.mass

    def update(self, delta_t):
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

