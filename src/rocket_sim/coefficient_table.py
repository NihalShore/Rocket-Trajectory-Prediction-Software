"""Validated one-dimensional coefficient tables with linear interpolation."""
from dataclasses import dataclass
import bisect
@dataclass(frozen=True)
class CoefficientPoint:
    independent: float
    coefficient: float
class CoefficientTable:
    def __init__(self,points,extrapolation="clamp"):
        self.points=tuple(CoefficientPoint(float(x),float(y)) for x,y in points)
        if len(self.points)<2: raise ValueError("at least two points required")
        if any(b.independent<=a.independent for a,b in zip(self.points,self.points[1:])): raise ValueError("abscissas must increase")
        if extrapolation not in {"clamp","linear","error"}: raise ValueError("invalid extrapolation mode")
        self.extrapolation=extrapolation; self._x=tuple(p.independent for p in self.points)
    def __call__(self,value):
        x=float(value)
        if x<self._x[0] or x>self._x[-1]:
            if self.extrapolation=="error": raise ValueError("query outside table")
            if self.extrapolation=="clamp": return self.points[0 if x<self._x[0] else -1].coefficient
            i=0 if x<self._x[0] else len(self.points)-2
        else: i=min(len(self.points)-2,max(0,bisect.bisect_right(self._x,x)-1))
        a,b=self.points[i],self.points[i+1]; f=(x-a.independent)/(b.independent-a.independent)
        return a.coefficient+f*(b.coefficient-a.coefficient)
    def derivative(self,value):
        x=float(value)
        i=0 if x<=self._x[0] else len(self.points)-2 if x>=self._x[-1] else bisect.bisect_right(self._x,x)-1
        a,b=self.points[i],self.points[i+1]
        return (b.coefficient-a.coefficient)/(b.independent-a.independent)
    @property
    def domain(self): return self._x[0],self._x[-1]
