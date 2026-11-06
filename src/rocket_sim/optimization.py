"""Derivative-free one-dimensional search utilities."""
from dataclasses import dataclass
@dataclass(frozen=True)
class SearchResult:
    x: float
    value: float
    evaluations: int
    converged: bool
def golden_section_minimize(function,lower,upper,tolerance=1e-5,max_iterations=200):
    if upper<=lower or tolerance<=0 or max_iterations<1: raise ValueError("invalid search controls")
    ratio=(5**.5-1)/2
    a=float(lower); b=float(upper); c=b-ratio*(b-a); d=a+ratio*(b-a)
    fc=float(function(c)); fd=float(function(d)); evaluations=2
    for _ in range(max_iterations):
        if abs(b-a)<=tolerance: break
        if fc<fd:
            b,d,fd=d,c,fc; c=b-ratio*(b-a); fc=float(function(c)); evaluations+=1
        else:
            a,c,fc=c,d,fd; d=a+ratio*(b-a); fd=float(function(d)); evaluations+=1
    x=(a+b)/2
    return SearchResult(x,float(function(x)),evaluations,abs(b-a)<=tolerance)
def grid_search(function,values):
    candidates=[(float(x),float(function(float(x)))) for x in values]
    if not candidates: raise ValueError("at least one candidate is required")
    x,value=min(candidates,key=lambda pair:pair[1])
    return SearchResult(x,value,len(candidates),True)
