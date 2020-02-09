from classes import Planet
from graphics import *
import time
from math import sqrt

win_w = 700
win_h = 700
win = GraphWin("n-body sim", win_w, win_h)
win.setBackground("black")
win.setCoords(-win_w/2, -win_h/2, win_w/2, win_h/2)

t_inc = 0.04
t_speed = 1

G = 1000

C1 = [0, 0]
my_planet1 = Planet("Sun", "yellow", 2500, C1, [0, 0])

C2 = [0, -300]
my_planet2 = Planet("Earth", "blue", 100, C2, [89, 0])

C3 = [0, 300]
my_planet3 = Planet("Venus", "brown", 100, C3, [-89, 0])

C4 = [0, -200]
my_planet4 = Planet("Moon", "gray", 1, C4, [100, 0])

C5 = [-200, 0]
my_planet5 = Planet("Phobos", "orange", 1, C5, [0, -100])

C6 = [200, 0]
my_planet6 = Planet("Ceres", "white", 2, C6, [0, 100])

C7 = [0, 200]
my_planet7 = Planet("Deimos", "green", 10, C7, [-100, 0])

planet_list = [my_planet1, my_planet2, my_planet3, my_planet4, my_planet5, my_planet6, my_planet7]

start_t = time.time()
curr_t = start_t
while win.checkMouse() is None:  # main program loop
    dt = time.time() - curr_t
    if dt > t_inc:
        dt = t_inc
        # print(my_planet2.vel)
        dt *= t_speed
        curr_t = time.time()
        win.delete("all")

        for planet in planet_list:
            circ = Circle(Point(planet.center[0], planet.center[1]), planet.radius)
            circ.setFill(planet.color)
            circ.draw(win)

            for other_planet in planet_list:
                if other_planet is not planet:
                   # print(planet.name, other_planet.name)
                    grav_force = [0, 0]
                    r_2 = ((planet.center[0] - other_planet.center[0]) ** 2) + \
                          ((planet.center[1] - other_planet.center[1]) ** 2)
                    r = sqrt(r_2)
                    if r < planet.radius + other_planet.radius:
                        if planet.mass == other_planet.mass:
                            planet_list.remove(other_planet)
                        elif planet.mass > other_planet.mass:
                            planet_list.remove(other_planet)
                        else:
                            planet_list.remove(planet)
                    else:
                        grav_force_magn = G * (planet.mass * other_planet.mass) / r_2
                        grav_force[0] = -((planet.center[0] - other_planet.center[0]) / sqrt(r_2)) * grav_force_magn
                        grav_force[1] = -((planet.center[1] - other_planet.center[1]) / sqrt(r_2)) * grav_force_magn
                        planet.apply_force(grav_force)

        for planet in planet_list:
            planet.update(dt)
            planet.clr_acc()

# win.getMouse() # Pause to view result
win.close()  # Close window when done
