"""Reproducible Monte Carlo wrappers for parameter sensitivity experiments."""
from dataclasses import dataclass
import numpy as np
@dataclass(frozen=True)
class MonteCarloSummary:
    parameter: str
    count: int
    mean: float
    standard_deviation: float
    minimum: float
    maximum: float
    percentile_05: float
    percentile_50: float
    percentile_95: float
def summarize(parameter,values):
    a=np.asarray(values,dtype=float)
    if a.size==0 or not np.all(np.isfinite(a)): raise ValueError("values must be finite and nonempty")
    return MonteCarloSummary(parameter,int(a.size),float(a.mean()),float(a.std(ddof=1) if a.size>1 else 0.),
        float(a.min()),float(a.max()),float(np.percentile(a,5)),float(np.percentile(a,50)),float(np.percentile(a,95)))
def sample_normal(mean,std,count,seed=None):
    if std<0 or count<1: raise ValueError("std must be nonnegative and count positive")
    return np.random.default_rng(seed).normal(mean,std,count)
def sample_uniform(low,high,count,seed=None):
    if high<low or count<1: raise ValueError("invalid bounds or count")
    return np.random.default_rng(seed).uniform(low,high,count)
def run_ensemble(config_factory,parameter_samples,metric="maximum_altitude"):
    """Run a caller-provided configuration factory over scalar samples."""
    values=[]
    for sample in parameter_samples:
        result=config_factory(float(sample))
        if not hasattr(result,"metrics") or not hasattr(result.metrics,metric): raise ValueError(f"unknown result metric: {metric}")
        values.append(float(getattr(result.metrics,metric)))
    return np.asarray(values)
