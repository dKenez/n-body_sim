from time import time
from Planet import Planet
from graphics import *
from math import sqrt


class System:
    """A class used to represent a System, which contains Planets."""
    __slots__ = ["name", "size", "max_planets", "win", "planets"]

    def __init__(self, name, max_planets=10, size=None):
        """Initialize the System object."""
        self.name = name
        self.max_planets = max_planets
        self.size = [800, 800] if size is None else size

        self.win = None
        self.planets = []

    def add_planets(self, *planet_list):
        """Add specified Planets to the System."""
        exceeded_limit = False
        for planet in planet_list:
            if len(self.planets) < self.max_planets:
                self.planets.append(planet)
                print("New Planet added:", planet.name)
            else:
                exceeded_limit = True
                print("Failed to add Planet without exceeding the System Planet limit:", planet.name)

        if exceeded_limit:
            print("\n System Planet limit:", self.max_planets)

    def remove_planets(self, *planet_list):
        """Remove specified Planets from System."""
        for planet in planet_list:
            if planet in self.planets:
                self.planets.remove(planet)
                print("Planet removed:", planet.name)
            else:
                print("Failed to remove Planet:", planet.name, "cannot be located in the System.", )

    def collide(self, planet_1: Planet, planet_2: Planet):
        """Handle collision of two Planets."""
        new_mass = planet_1.mass + planet_2.mass

        new_com = [
            (planet_1.mass * planet_1.center[0] + planet_2.mass * planet_2.center[0]) / new_mass,
            (planet_1.mass * planet_1.center[1] + planet_2.mass * planet_2.center[1]) / new_mass
        ]

        new_vel = [
            (planet_1.mass * planet_1.vel[0] + planet_2.mass * planet_2.vel[0]) / new_mass,
            (planet_1.mass * planet_1.vel[1] + planet_2.mass * planet_2.vel[1]) / new_mass
        ]

        if planet_1.mass > planet_2.mass:
            new_name = planet_1.name + "-" + planet_2.name
            new_color = planet_1.color
        else:
            new_name = planet_2.name + "-" + planet_1.name
            new_color = planet_2.color

        new_planet = Planet(new_name, new_color, new_mass, new_com, new_vel)
        self.remove_planets(planet_1, planet_2)
        self.add_planets(new_planet)

    def set_default_system(self):
        """Add the default Planets to the System."""
        self.remove_planets(*self.planets)
        default_planets = [
            Planet("Sun", "yellow", 2500),
            Planet("Earth", "blue", 100, [0, -300], [89, 0]),
            Planet("Venus", "brown", 100, [0, 300], [-89, 0]),
            Planet("Moon", "gray", 1, [0, -200], [100, 0]),
            Planet("Phobos", "orange", 1, [-200, 0], [0, -100]),
            Planet("Ceres", "white", 2, [200, 0], [0, 100]),
            Planet("Deimos", "green", 10, [0, 200], [-100, 0])
        ]
        self.add_planets(*default_planets)

    def draw_planet(self, planet):
        """Draw Planet using graphics.py."""
        circle = Circle(Point(planet.center[0], planet.center[1]), planet.radius)
        circle.setFill(planet.color)
        circle.draw(self.win)

    def simulate_system(self, grav_coeff=1000, sim_speed=1, max_sim_t=600, t_inc=0.04):
        """Run the simulation of the System with the specified parameters."""
        win_w = int(self.size[0])
        win_h = int(self.size[1])
        self.win = GraphWin(self.name, win_w, win_h)
        self.win.setBackground("black")
        self.win.setCoords(-win_w / 2, -win_h / 2, win_w / 2, win_h / 2)

        sim_start_t = time.time()
        curr_t = sim_start_t
        while self.win.checkMouse() is None and (time.time() - sim_start_t < max_sim_t):  # main program loop
            dt = time.time() - curr_t
            if dt > t_inc:
                curr_t = time.time()
                dt = t_inc
                dt *= sim_speed

                self.win.delete("all")

                for planet in self.planets:
                    self.draw_planet(planet)

                    for other_planet in self.planets:
                        if other_planet is not planet:
                            grav_force = [0, 0]

                            d_x = other_planet.center[0] - planet.center[0]
                            d_y = other_planet.center[1] - planet.center[1]

                            r_sqrd = d_x ** 2 + d_y ** 2
                            r = sqrt(r_sqrd)

                            if r < planet.radius + other_planet.radius:
                                self.collide(planet, other_planet)
                                break
                            else:
                                grav_force_magn = grav_coeff * (planet.mass * other_planet.mass) / r_sqrd
                                grav_force[0] = grav_force_magn * (d_x / r)
                                grav_force[1] = grav_force_magn * (d_y / r)
                                planet.apply_force(grav_force)

                for planet in self.planets:
                    planet.update(dt)
                    planet.clr_acc()

        # win.getMouse() # Pause to view result
        self.win.close()  # Close window when done
        sim_t = time.time() - sim_start_t
        end_message = "\nSimulation of {0} finished\nSimulation time: {1:.2f} seconds\nPlanets simulated: {2}"
        end_message = end_message.format(self.name, sim_t, len(self.planets))
        print(end_message)
