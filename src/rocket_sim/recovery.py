"""Parachute / recovery phase.

After apogee (or a timer) we can deploy a chute and fall under a higher Cd.
Very rough — no reefing schedules, just a Cd bump and maybe a delayed main.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Chute:
    name: str
    area: float
    cd: float = 1.5
    deploy_altitude: float | None = None
    deploy_time: float | None = None
    reefing_factor: float = 1.0

    def drag_force(self, density, speed):
        q = 0.5 * density * speed * speed
        return q * self.cd * self.area * self.reefing_factor


@dataclass
class RecoverySystem:
    chutes: list
    deployed: list = None

    def __post_init__(self):
        if self.deployed is None:
            self.deployed = []

    def maybe_deploy(self, t, alt):
        for c in self.chutes:
            if c in self.deployed:
                continue
            by_time = c.deploy_time is not None and t >= c.deploy_time
            by_alt = c.deploy_altitude is not None and alt <= c.deploy_altitude
            if c.deploy_time is None and c.deploy_altitude is None:
                continue
            if by_time or by_alt:
                self.deployed.append(c)

    def total_drag(self, density, speed):
        f = 0.0
        for c in self.deployed:
            f += c.drag_force(density, speed)
        return f

    @property
    def is_deployed(self):
        return len(self.deployed) > 0


def simple_dual_deploy(drogue_area=0.5, main_area=5.0, main_alt=300.0):
    drogue = Chute("drogue", drogue_area, cd=1.2, deploy_altitude=1e9)
    main = Chute("main", main_area, cd=2.0, deploy_altitude=main_alt)
    return RecoverySystem([drogue, main])
