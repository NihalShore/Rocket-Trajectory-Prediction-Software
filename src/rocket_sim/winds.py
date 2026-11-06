"""Simple wind profiles for sensitivity studies (not operational weather data)."""
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class WindVector:
    east: float
    north: float
    vertical: float=0.
    @property
    def speed(self): return math.sqrt(self.east**2+self.north**2+self.vertical**2)
class WindProfile:
    def __init__(self,levels):
        self.levels=tuple(sorted((float(h),float(e),float(n),float(u)) for h,e,n,u in levels))
        if not self.levels: raise ValueError("at least one wind level is required")
        if any(b[0]<=a[0] for a,b in zip(self.levels,self.levels[1:])): raise ValueError("wind altitudes must be unique")
    def at(self,altitude):
        if altitude<=self.levels[0][0]:
            _,e,n,u=self.levels[0]; return WindVector(e,n,u)
        if altitude>=self.levels[-1][0]:
            _,e,n,u=self.levels[-1]; return WindVector(e,n,u)
        for a,b in zip(self.levels,self.levels[1:]):
            if a[0]<=altitude<=b[0]:
                f=(altitude-a[0])/(b[0]-a[0])
                return WindVector(a[1]+f*(b[1]-a[1]),a[2]+f*(b[2]-a[2]),a[3]+f*(b[3]-a[3]))
        raise RuntimeError("wind interpolation failed")
def calm_wind(): return WindProfile([(0.,0.,0.,0.),(100000.,0.,0.,0.)])
