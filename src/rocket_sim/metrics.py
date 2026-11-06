"""Peak values and approximate ascent-loss accounting."""
from dataclasses import dataclass
from .constants import G0
from .state import TrajectorySample
@dataclass(frozen=True)
class TrajectoryMetrics:
    maximum_altitude: float
    maximum_speed: float
    maximum_mach: float
    maximum_dynamic_pressure: float
    maximum_acceleration: float
    burnout_time: float|None
    apogee_time: float|None
    downrange_at_apogee: float|None
    final_mass: float
    ideal_delta_v: float
    estimated_gravity_loss: float
    estimated_drag_loss: float
def compute_metrics(samples,ideal_delta_v=0.):
    if not samples: raise ValueError("samples cannot be empty")
    accel=[]; gravity_loss=0.; drag_loss=0.
    for a,b in zip(samples,samples[1:]):
        dt=b.time-a.time
        if dt<=0: continue
        accel.append(abs(b.state.speed-a.state.speed)/dt)
        gravity_loss+=G0*max(0.,b.state.vertical_velocity/max(b.state.speed,1e-9))*dt
        drag_loss+=max(0.,b.drag)/max(b.state.mass,1e-9)*dt
    burnout=next((s.time for s in samples if s.event=="burnout"),None)
    apogee=next((s.time for s in samples if s.event=="apogee"),None)
    ap= min(samples,key=lambda s:abs(s.time-apogee)) if apogee is not None else None
    return TrajectoryMetrics(max(s.state.altitude for s in samples),max(s.state.speed for s in samples),max(s.mach for s in samples),max(s.dynamic_pressure for s in samples),max(accel,default=0.),burnout,apogee,ap.state.downrange if ap else None,samples[-1].state.mass,ideal_delta_v,gravity_loss,drag_loss)
