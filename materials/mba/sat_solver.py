from z3 import *

x,y = BitVecs('x y', 32) # we're working on 32 bit
func_one = (x * x * 7) - 1 # we add our equations
func_two = (y*y)

solver = Solver() # create new solver object
solver.add(func_one == func_two) # and we add the equation model we want to check to the solver object

if solver.check() == unsat: 
    print("returned unsat")
else:
    print(solver.model())