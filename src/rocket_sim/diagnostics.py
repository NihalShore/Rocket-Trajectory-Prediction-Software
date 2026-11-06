"""Trajectory sanity checks."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    message: str
    sample_index: int|None=None
def validate_samples(samples):
    issues=[]
    if not samples: return [Diagnostic("error","EMPTY_RESULT","No samples were produced.")]
    for i,s in enumerate(samples):
        if s.state.mass<=0: issues.append(Diagnostic("error","NONPOSITIVE_MASS","Mass must remain positive.",i))
        if s.state.altitude< -1e-6: issues.append(Diagnostic("warning","BELOW_GROUND","Trajectory is below ground.",i))
        if s.dynamic_pressure<0 or s.drag<0: issues.append(Diagnostic("error","NEGATIVE_AERO_LOAD","Aerodynamic load cannot be negative.",i))
        if i and s.time<=samples[i-1].time: issues.append(Diagnostic("error","TIME_ORDER","Times must increase.",i))
        if i and s.state.mass>samples[i-1].state.mass+1e-6: issues.append(Diagnostic("warning","MASS_INCREASE","Mass increased between samples.",i))
    return issues
def assert_valid_samples(samples):
    errors=[d for d in validate_samples(samples) if d.severity=="error"]
    if errors: raise ValueError("; ".join(f"{d.code}: {d.message}" for d in errors))
