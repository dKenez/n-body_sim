from classes import Planet
from graphics import *

win_w = 500
win_h = 500
win = GraphWin("n-body sim", win_w, win_h)
win.setBackground("black")
win.setCoords(0, 0, win_w, win_h)

t_inc = 0.01

C1 = [50, 200]
my_planet1 = Planet("mars", 5, C1, [20, 2])

C2 = [50, 10]
my_planet2 = Planet("earth", 8, C2, [1, 10])

planet_list = [my_planet1, my_planet2]

start_t = time.time()
curr_t = start_t
while win.checkMouse() is None:  # main program loop
    dt = time.time() - curr_t
    if dt > t_inc:
        win.delete("all")
        curr_t = time.time()

        for planet in planet_list:
            planet.update(dt)

            circ = Circle(Point(planet.center[0], planet.center[1]), 10)
            circ.setFill("white")
            circ.draw(win)





# win.getMouse() # Pause to view result
win.close()    # Close window when done

