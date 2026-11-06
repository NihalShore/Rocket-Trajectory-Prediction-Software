"""Demonstrate adaptive integration on a known scalar system."""
import numpy as np
from rocket_sim.adaptive import integrate_adaptive
def derivative(time,state): return np.array([-0.4*state[0]])
result=integrate_adaptive(derivative,[1.],0.,8.,.5,absolute_tolerance=1e-10,relative_tolerance=1e-8)
exact=np.exp(-.4*8.)
print("computed:",result.states[-1,0])
print("exact:",exact)
print("accepted/rejected:",result.accepted_steps,result.rejected_steps)
