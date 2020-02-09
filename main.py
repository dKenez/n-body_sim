from System import System

my_sys = System("Solar System")

my_sys.set_default_system()
my_sys.simulate_system(grav_coeff=1000, max_sim_t=10)
