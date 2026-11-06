"""Compare numerical integration choices on a scalar decay problem."""
import numpy as np
from rocket_sim.integrators import integrate_fixed
def rhs(time,state): return -0.15*state
for method in ("euler","heun","rk4"):
    times,states=integrate_fixed(rhs,np.array([1.]),0.,10.,.25,method)
    exact=np.exp(-.15*times[-1])
    print(method,"computed",states[-1,0],"exact",exact,"absolute error",abs(states[-1,0]-exact))
